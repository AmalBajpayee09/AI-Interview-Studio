"""Transactional SQLite storage with idempotent schema migration."""
import json
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from . import config

_LOCK = threading.RLock()

@contextmanager
def connect():
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with _LOCK:
        db = sqlite3.connect(str(config.DB_PATH), timeout=10)
        try:
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA journal_mode=WAL')
            db.execute('PRAGMA foreign_keys=ON')
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

def initialize():
    with connect() as db:
        version = db.execute('PRAGMA user_version').fetchone()[0]
        if version < 1:
            db.executescript('''
              CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, title TEXT NOT NULL, created REAL NOT NULL, updated REAL NOT NULL);
              CREATE TABLE IF NOT EXISTS turns (id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE, question TEXT NOT NULL, answer TEXT NOT NULL, mode TEXT NOT NULL, provider TEXT NOT NULL, elapsed_ms INTEGER NOT NULL, created REAL NOT NULL);
              CREATE INDEX IF NOT EXISTS turns_by_session ON turns(session_id,created);
              CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, filename TEXT NOT NULL, content TEXT NOT NULL, created REAL NOT NULL);
              CREATE TABLE IF NOT EXISTS assessments (id TEXT PRIMARY KEY, title TEXT NOT NULL, questions_json TEXT NOT NULL, duration_seconds INTEGER NOT NULL, created REAL NOT NULL);
              CREATE TABLE IF NOT EXISTS attempts (id TEXT PRIMARY KEY, assessment_id TEXT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE, answers_json TEXT NOT NULL, started REAL NOT NULL, finished REAL, result_json TEXT);
              PRAGMA user_version=1;
            ''')
        if version < 2:
            db.execute('CREATE INDEX IF NOT EXISTS session_updated ON sessions(updated DESC)')
            db.execute('PRAGMA user_version=2')
        if version < 3:
            db.execute("""CREATE TABLE IF NOT EXISTS assessment_drafts (
                assessment_id TEXT PRIMARY KEY REFERENCES assessments(id) ON DELETE CASCADE,
                answers_json TEXT NOT NULL, review_json TEXT NOT NULL,
                started REAL NOT NULL, updated REAL NOT NULL)""")
            db.execute('CREATE INDEX IF NOT EXISTS drafts_by_updated ON assessment_drafts(updated DESC)')
            db.execute('PRAGMA user_version=3')
        if version < 4:
            db.execute('CREATE TABLE IF NOT EXISTS settings (name TEXT PRIMARY KEY, value TEXT NOT NULL)')
            db.execute('PRAGMA user_version=4')

def session_create(title='Practice session'):
    sid = str(uuid.uuid4()); now = time.time()
    with connect() as db:
        db.execute('INSERT INTO sessions VALUES (?,?,?,?)',(sid,title[:120],now,now))
    return {'id':sid, 'title':title[:120], 'created':now, 'updated':now}

def sessions():
    with connect() as db:
        return [dict(r) for r in db.execute('SELECT * FROM sessions ORDER BY updated DESC LIMIT 100')]

def get_turns(sid):
    with connect() as db:
        if not db.execute('SELECT 1 FROM sessions WHERE id=?',(sid,)).fetchone():
            raise ValueError('Unknown session')
        return [dict(r) for r in db.execute('SELECT * FROM turns WHERE session_id=? ORDER BY created,id',(sid,))]

def save_turn(sid, question, answer, mode, provider, elapsed_ms):
    now = time.time(); tid = str(uuid.uuid4())
    with connect() as db:
        db.execute('INSERT INTO turns VALUES (?,?,?,?,?,?,?,?)', (tid,sid,question[:10000],answer[:50000],mode,provider,elapsed_ms,now))
        if db.execute('UPDATE sessions SET updated=? WHERE id=?',(now,sid)).rowcount != 1:
            raise ValueError('Unknown session')
    return tid

def delete_session(sid):
    with connect() as db: return db.execute('DELETE FROM sessions WHERE id=?',(sid,)).rowcount > 0

def save_document(filename,content):
    docid = str(uuid.uuid4())
    with connect() as db:
        db.execute('INSERT INTO documents VALUES (?,?,?,?)',(docid,filename[:150],content[:150000],time.time()))
    return docid

def documents(include_content=False):
    cols = "id,filename,content,created" if include_content else "id,filename,created,length(content) size"
    with connect() as db: return [dict(r) for r in db.execute(f"SELECT {cols} FROM documents ORDER BY created DESC")]

def delete_document(did):
    with connect() as db: return db.execute('DELETE FROM documents WHERE id=?',(did,)).rowcount > 0

def retrieved_context(query):
    terms = set(w.lower() for w in query.split() if len(w) >= 4)
    with connect() as db:
        rows = db.execute('SELECT filename,content FROM documents ORDER BY created DESC LIMIT 30').fetchall()
    scored = []
    for row in rows:
        chunks = [row['content'][i:i+1400] for i in range(0, min(len(row['content']), 90000), 1100)]
        for chunk in chunks:
            score = sum(chunk.lower().count(t) for t in terms)
            if score: scored.append((score, row['filename'], chunk))
    scored.sort(reverse=True)
    return '\n'.join(f'{name}: {chunk}' for _,name,chunk in scored[:3])[:3500]

def create_assessment(title,questions,duration_seconds):
    aid = str(uuid.uuid4())
    with connect() as db:
        db.execute('INSERT INTO assessments VALUES (?,?,?,?,?)',(aid,title,json.dumps(questions),duration_seconds,time.time()))
    return aid

def list_assessments():
    with connect() as db:
        return [{**dict(r),'questions':json.loads(r['questions_json'])} for r in db.execute('SELECT * FROM assessments ORDER BY created DESC')]

def assessment_by_id(aid):
    with connect() as db:
        row = db.execute('SELECT * FROM assessments WHERE id=?',(aid,)).fetchone()
    if not row: raise ValueError('Unknown assessment')
    return {**dict(row),'questions':json.loads(row['questions_json'])}

def save_attempt(aid, answers, result, started):
    attempt_id = str(uuid.uuid4()); now = time.time()
    with connect() as db:
        db.execute('INSERT INTO attempts VALUES (?,?,?,?,?,?)',(attempt_id,aid,json.dumps(answers),started,now,json.dumps(result)))
    return attempt_id

def stats():
    with connect() as db:
        s=db.execute('SELECT count(*) FROM sessions').fetchone()[0]
        t=db.execute('SELECT count(*),coalesce(avg(elapsed_ms),0) FROM turns').fetchone()
        attempts=db.execute('SELECT result_json FROM attempts WHERE result_json IS NOT NULL').fetchall()
    results=[json.loads(row[0]) for row in attempts]
    return {'sessions':s,'questions':t[0],'average_answer_ms':round(t[1]),'assessments_completed':len(results),'average_score_pct':round(sum(r['percent'] for r in results)/len(results),1) if results else None}

def cleanup():
    cutoff=time.time()-config.RETENTION_DAYS*86400
    with connect() as db:
        db.execute('DELETE FROM sessions WHERE updated < ?', (cutoff,))
        db.execute('DELETE FROM documents WHERE created < ?', (cutoff,))
        db.execute('DELETE FROM assessments WHERE created < ?', (cutoff,))


def save_assessment_draft(aid, answers, review, started):
    # Transactional upsert; never touches finalized attempt records.
    with connect() as database:
        if not database.execute('SELECT 1 FROM assessments WHERE id=?',(aid,)).fetchone():
            raise ValueError('Unknown assessment')
        database.execute('''INSERT INTO assessment_drafts
            (assessment_id,answers_json,review_json,started,updated) VALUES(?,?,?,?,?)
            ON CONFLICT(assessment_id) DO UPDATE SET
            answers_json=excluded.answers_json,review_json=excluded.review_json,
            started=excluded.started,updated=excluded.updated''',
            (aid,json.dumps(answers),json.dumps(review),started,time.time()))
    return {'saved':True,'updated':time.time()}

def get_assessment_draft(aid):
    with connect() as database:
        row=database.execute('SELECT * FROM assessment_drafts WHERE assessment_id=?',(aid,)).fetchone()
    if not row: return None
    return {'assessment_id':aid,'answers':json.loads(row['answers_json']),
            'review':json.loads(row['review_json']),'started':row['started'],'updated':row['updated']}

def remove_assessment_draft(aid):
    with connect() as database:
        return bool(database.execute('DELETE FROM assessment_drafts WHERE assessment_id=?',(aid,)).rowcount)

def database_backup(destination):
    '''SQLite online backup API makes a transactionally consistent copy under WAL.'''
    import sqlite3
    with connect() as source:
        target=sqlite3.connect(str(destination))
        try:
            source.backup(target)
            assert target.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        finally: target.close()


def setting(name, default=None):
    with connect() as database:
        row=database.execute('SELECT value FROM settings WHERE name=?',(name,)).fetchone()
    return row[0] if row else default

def set_setting(name,value):
    with connect() as database:
        database.execute('INSERT INTO settings (name,value) VALUES (?,?) ON CONFLICT(name) DO UPDATE SET value=excluded.value',(name,value))
