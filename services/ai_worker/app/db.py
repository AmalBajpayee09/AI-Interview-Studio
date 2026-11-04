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
        if version < 5:
            db.execute("""CREATE TABLE IF NOT EXISTS transcript_segments (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                text TEXT NOT NULL,
                source_id TEXT NOT NULL,
                speaker TEXT NOT NULL DEFAULT 'unknown',
                speaker_confidence REAL,
                language TEXT,
                started_at REAL,
                ended_at REAL,
                created REAL NOT NULL
            )""")
            db.execute('CREATE INDEX IF NOT EXISTS transcripts_by_session ON transcript_segments(session_id,created,id)')
            db.execute('PRAGMA user_version=5')
        if version < 6:
            # Preserve historical submissions; new requests carry idempotency receipts.
            db.execute("""CREATE TABLE IF NOT EXISTS attempt_receipts (
                assessment_id TEXT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
                started REAL NOT NULL,
                attempt_id TEXT NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
                PRIMARY KEY (assessment_id, started))""")
            db.execute('CREATE INDEX IF NOT EXISTS receipts_by_attempt ON attempt_receipts(attempt_id)')
            db.execute('PRAGMA user_version=6')
        if version < 7:
            # Existing assessments remain legacy practice; new timed assessments
            # explicitly opt in to server-owned clock and grading rules.
            columns = {row['name'] for row in db.execute('PRAGMA table_info(assessments)')}
            if 'require_start' not in columns:
                db.execute('ALTER TABLE assessments ADD COLUMN require_start INTEGER NOT NULL DEFAULT 0')
            if 'negative_marking' not in columns:
                db.execute('ALTER TABLE assessments ADD COLUMN negative_marking REAL NOT NULL DEFAULT 0.25')
            if 'cutoff_pct' not in columns:
                db.execute('ALTER TABLE assessments ADD COLUMN cutoff_pct REAL')
            db.execute('PRAGMA user_version=7')
        # Older v6 databases were created with AI usage, but some migration paths
        # may not have the table. Keep this idempotent repair independent of the
        # schema-version marker; never lower user_version after the v7 migration.
        db.execute("""CREATE TABLE IF NOT EXISTS ai_usage (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                first_token_ms INTEGER,
                total_ms INTEGER NOT NULL,
                output_characters INTEGER NOT NULL,
                created REAL NOT NULL
            )""")
        db.execute('CREATE INDEX IF NOT EXISTS ai_usage_by_session ON ai_usage(session_id,created)')

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

def document_by_id(did):
    with connect() as database:
        item=database.execute('SELECT id,filename,content,created FROM documents WHERE id=?',(did,)).fetchone()
    if not item:raise ValueError('Unknown document')
    return dict(item)

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

def create_assessment(title,questions,duration_seconds,*,require_start=False,negative_marking=0.25,cutoff_pct=None):
    aid = str(uuid.uuid4())
    with connect() as db:
        db.execute('''INSERT INTO assessments
            (id,title,questions_json,duration_seconds,created,require_start,negative_marking,cutoff_pct)
            VALUES (?,?,?,?,?,?,?,?)''',
            (aid,title,json.dumps(questions),duration_seconds,time.time(),int(require_start),negative_marking,cutoff_pct))
    return aid

def list_assessments():
    with connect() as db:
        return [{**dict(r),'questions':json.loads(r['questions_json'])} for r in db.execute('''
            SELECT a.*, (SELECT COUNT(*) FROM attempts t WHERE t.assessment_id=a.id) AS attempt_count
            FROM assessments a ORDER BY a.created DESC''')]

def assessment_by_id(aid):
    with connect() as db:
        row = db.execute('SELECT * FROM assessments WHERE id=?',(aid,)).fetchone()
    if not row: raise ValueError('Unknown assessment')
    return {**dict(row),'questions':json.loads(row['questions_json'])}

def latest_assessment_result(aid):
    """Retrieve the persisted final result for desktop restart/review.

    Do not expose answer keys for assessments still in progress. Only completed
    attempt receipts are visible here. The authenticated local API is single-user.
    """
    with connect() as database:
        existing=database.execute('SELECT 1 FROM assessments WHERE id=?',(aid,)).fetchone()
        if not existing:raise ValueError('Unknown assessment')
        row=database.execute("""SELECT a.id,a.started,a.finished,a.result_json
            FROM attempts a JOIN attempt_receipts r ON r.attempt_id=a.id
            WHERE a.assessment_id=? AND a.result_json IS NOT NULL
            ORDER BY a.finished DESC,a.id DESC LIMIT 1""",(aid,)).fetchone()
    if row is None:return None
    return {'attempt_id':row['id'],'started':row['started'],'finished':row['finished'],
            'result':json.loads(row['result_json'])}

def save_attempt(aid, answers, result, started):
    attempt_id = str(uuid.uuid4()); now = time.time()
    with connect() as db:
        db.execute('INSERT INTO attempts VALUES (?,?,?,?,?,?)',(attempt_id,aid,json.dumps(answers),started,now,json.dumps(result)))
    return attempt_id

def start_assessment(aid):
    """Store a server start time once and preserve recoverable quiz drafts."""
    with connect() as database:
        if not database.execute('SELECT 1 FROM assessments WHERE id=?',(aid,)).fetchone():
            raise ValueError('Unknown assessment')
        existing=database.execute('SELECT * FROM assessment_drafts WHERE assessment_id=?',(aid,)).fetchone()
        if existing:
            return {'assessment_id':aid,'answers':json.loads(existing['answers_json']),
                    'review':json.loads(existing['review_json']),'started':existing['started'],
                    'updated':existing['updated'],'recovered':True}
        started=time.time()
        database.execute('INSERT INTO assessment_drafts VALUES (?,?,?,?,?)',(aid,'{}','[]',started,started))
        return {'assessment_id':aid,'answers':{},'review':[],'started':started,
                'updated':started,'recovered':False}

def completed_attempt(aid, started):
    with connect() as database:
        row=database.execute("""SELECT a.id,a.result_json FROM attempt_receipts r
            JOIN attempts a ON a.id=r.attempt_id WHERE r.assessment_id=? AND r.started=?""",
            (aid,started)).fetchone()
    return ({**json.loads(row['result_json']),'attempt_id':row['id'],'duplicate_submission':True}
            if row else None)


def finalize_attempt(aid,answers,result,started):
    """Transactional receipt and draft cleanup: retries cannot alter final grades."""
    with connect() as database:
        previous=database.execute("""SELECT a.id,a.result_json FROM attempt_receipts r
            JOIN attempts a ON a.id=r.attempt_id WHERE r.assessment_id=? AND r.started=?""",
            (aid,started)).fetchone()
        if previous:
            return {**json.loads(previous['result_json']),'attempt_id':previous['id'],'duplicate_submission':True}
        attempt_id=str(uuid.uuid4());finished=time.time()
        database.execute('INSERT INTO attempts VALUES (?,?,?,?,?,?)',
                         (attempt_id,aid,json.dumps(answers),started,finished,json.dumps(result)))
        database.execute('INSERT INTO attempt_receipts VALUES (?,?,?)',(aid,started,attempt_id))
        database.execute('DELETE FROM assessment_drafts WHERE assessment_id=? AND started=?',(aid,started))
    return {**result,'attempt_id':attempt_id,'duplicate_submission':False}

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
    """Autosave without allowing a client to rewrite a server-established start time.

    Older clients can create a draft directly; an existing draft always owns
    its original start. Late autosaves cannot modify its saved answers.
    """
    with connect() as database:
        row=database.execute('SELECT duration_seconds FROM assessments WHERE id=?',(aid,)).fetchone()
        if not row: raise ValueError('Unknown assessment')
        existing=database.execute('SELECT started FROM assessment_drafts WHERE assessment_id=?',(aid,)).fetchone()
        if existing is not None:
            if abs(float(existing['started'])-float(started))>0.001:
                raise ValueError('Assessment start timestamp does not match the server record')
            started=float(existing['started'])
        if time.time()>started+float(row['duration_seconds']):
            raise ValueError('Assessment time has expired; saved answers cannot be changed')
        database.execute('''INSERT INTO assessment_drafts
            (assessment_id,answers_json,review_json,started,updated) VALUES(?,?,?,?,?)
            ON CONFLICT(assessment_id) DO UPDATE SET
            answers_json=excluded.answers_json,review_json=excluded.review_json,
            updated=excluded.updated''',
            (aid,json.dumps(answers),json.dumps(review),started,time.time()))
        return {'saved':True,'updated':time.time(),'started':started}

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


def save_transcript(sid, text, source_id, speaker='unknown', confidence=None,
                    language=None, started_at=None, ended_at=None):
    """Consent-based transcript persistence; no raw audio is written."""
    now=time.time()
    tid=str(uuid.uuid4())
    with connect() as database:
        if not database.execute('SELECT 1 FROM sessions WHERE id=?',(sid,)).fetchone():
            raise ValueError('Unknown session')
        database.execute("INSERT INTO transcript_segments VALUES (?,?,?,?,?,?,?,?,?,?)",
            (tid,sid,text,source_id,speaker,confidence,language,started_at,ended_at,now))
        # Keep only latest 500 segments per session; older events are removed.
        database.execute("""DELETE FROM transcript_segments WHERE session_id=? AND id NOT IN
            (SELECT id FROM transcript_segments WHERE session_id=? ORDER BY created DESC, rowid DESC LIMIT 500)""",(sid,sid))
        database.execute('UPDATE sessions SET updated=? WHERE id=?',(now,sid))
    return {'id':tid,'saved':True}


def transcripts(sid, limit=100):
    with connect() as database:
        if not database.execute('SELECT 1 FROM sessions WHERE id=?',(sid,)).fetchone():
            raise ValueError('Unknown session')
        rows=database.execute("""SELECT * FROM transcript_segments WHERE session_id=?
            ORDER BY created DESC,rowid DESC LIMIT ?""",(sid,limit)).fetchall()
    return [dict(row) for row in reversed(rows)]


def clear_transcripts(sid):
    with connect() as database:
        if not database.execute('SELECT 1 FROM sessions WHERE id=?',(sid,)).fetchone():
            raise ValueError('Unknown session')
        return database.execute('DELETE FROM transcript_segments WHERE session_id=?',(sid,)).rowcount


def save_ai_usage(sid, provider, model, first_token_ms, total_ms, output_characters):
    with connect() as database:
        database.execute('INSERT INTO ai_usage VALUES(?,?,?,?,?,?,?,?)',
                         (str(uuid.uuid4()),sid,provider,model,first_token_ms,total_ms,
                          output_characters,time.time()))

def ai_usage(sid=None):
    with connect() as database:
        if sid is not None:
            if not database.execute('SELECT 1 FROM sessions WHERE id=?',(sid,)).fetchone():
                raise ValueError('Unknown session')
            rows=database.execute('SELECT session_id,provider,model,first_token_ms,total_ms,output_characters,created FROM ai_usage WHERE session_id=? ORDER BY created DESC LIMIT 200',(sid,))
        else:
            rows=database.execute('SELECT session_id,provider,model,first_token_ms,total_ms,output_characters,created FROM ai_usage ORDER BY created DESC LIMIT 200')
        return [dict(r) for r in rows]
