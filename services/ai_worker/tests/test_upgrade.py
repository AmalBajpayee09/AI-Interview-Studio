"""Regression/integration tests added for completion add-on v0.2.0."""
import sqlite3
import time
from pathlib import Path
from app import db,logic
from app.sql_lab import execute_readonly, SQLPracticeError


def test_sql_joins(client):
    response=client.post('/api/sql/query',json={'query':'SELECT d.name, count(e.id) n FROM departments d LEFT JOIN employees e ON d.id=e.department_id GROUP BY d.id ORDER BY d.id'})
    assert response.status_code==200, response.text
    assert response.json()['rows']==[['Engineering',2],['Sales',2],['Design',1]]
    assert response.json()['verified'].startswith('Executed')


def test_sql_read_only(client):
    candidates=['DROP TABLE employees', 'DELETE FROM employees',
                'WITH v AS (DELETE FROM employees RETURNING *) SELECT * FROM v',
                'SELECT load_extension("x")', 'PRAGMA database_list',
                'ATTACH DATABASE "/tmp/user.db" AS local',
                'SELECT 1; DELETE FROM employees',
                'SELECT randomblob(200000000)']
    for query in candidates:
        response=client.post('/api/sql/query',json={'query':query})
        assert response.status_code==400,(query,response.text)
    assert client.post('/api/sql/query',json={'query':'SELECT count(*) FROM employees'}).json()['rows']==[[6]]


def test_sql_schema_and_limits(client):
    schema=client.get('/api/sql/schema').json()
    assert schema['read_only'] and len(schema['tables'])==3
    assert client.post('/api/sql/query',json={'query':'SELECT * FROM employees','max_rows':1}).json()['truncated']
    assert client.post('/api/sql/query',json={'query':'SELECT 1','max_rows':101}).status_code==422


def test_sql_timeout():
    import pytest
    with pytest.raises(SQLPracticeError):
        execute_readonly('WITH RECURSIVE x(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM x WHERE n<999999999) SELECT max(n) FROM x',timeout_ms=15)


def test_draft_restore_delete_submit(client):
    assessment=client.get('/api/assessments').json()[0]
    aid=assessment['id'];started=time.time()
    url=f'/api/assessments/{aid}/draft'
    assert client.get(url).json()['draft'] is None
    data={'answers':{'q1':'B'},'review':['q2'],'started':started}
    assert client.post(url,json=data).status_code==200
    assert client.get(url).json()['draft']['answers']=={'q1':'B'}
    data['answers']={'q1':'A','q2':'C'}
    assert client.post(url,json=data).status_code==200
    assert client.get(url).json()['draft']['answers']==data['answers']
    assert client.post(url,json={'answers':{'not-a-question':'B'},'started':started}).status_code==400
    assert client.post(f'/api/assessments/{aid}/submit',json={'answers':data['answers'],'started':started}).status_code==200
    assert client.get(url).json()['draft'] is None


def test_draft_survives_db_reinit(client):
    aid=client.get('/api/assessments').json()[0]['id'];now=time.time()
    db.save_assessment_draft(aid,{'q2':'C'},['q1'],now)
    db.initialize()  # simulates app process restart/migration, no destructive reset
    assert db.get_assessment_draft(aid)['answers']=={'q2':'C'}


def test_sqlite_online_backup(client,tmp_path):
    client.post('/api/sessions',json={'title':'Saved context'})
    data=client.get('/api/backup/database')
    assert data.status_code==200
    assert data.content.startswith(b'SQLite format 3')
    target=tmp_path/'backup.sqlite3';target.write_bytes(data.content)
    with sqlite3.connect(target) as con:
        assert con.execute('SELECT COUNT(*) FROM sessions').fetchone()[0]==1
        assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert con.execute('PRAGMA user_version').fetchone()[0]==5


def test_schema_compatibility_existing_v2(client):
    with db.connect() as con:
        assert con.execute('PRAGMA user_version').fetchone()[0]==5
        assert con.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='turns'").fetchone()[0]==1


def test_unicode_sql(client):
    result=client.post('/api/sql/query',json={'query':"SELECT 'नमस्ते' AS message"})
    assert result.status_code==200
    assert result.json()['rows']==[['नमस्ते']]


def test_assessment_duplicate_answer_labels_rejected(client):
    original={'id':'q1','stem':'One?','options':[{'label':'A','text':'a'},{'label':'A','text':'b'}],'correct':'A'}
    res=client.post('/api/assessments',json={'title':'Invalid','duration_seconds':120,'questions':[original]})
    assert res.status_code==400
    original['options'][1]['label']='B'
    assert client.post('/api/assessments',json={'title':'Valid','duration_seconds':120,'questions':[original]}).status_code==200


def test_assessment_question_ids_are_unique(client):
    q={'id':'q1','stem':'What?','options':[{'label':'A','text':'Yes'},{'label':'B','text':'No'}],'correct':'B'}
    assert client.post('/api/assessments',json={'title':'Invalid','duration_seconds':120,'questions':[q,q]}).status_code==400


def test_resource_profile_persists(client):
    assert client.get('/api/resource').json()['mode']=='balanced'
    result=client.post('/api/resource',json={'mode':'battery-saver'})
    assert result.status_code==200
    assert result.json()['recommended_max_parallel_requests']==1
    db.initialize()
    assert client.get('/api/resource').json()['mode']=='battery-saver'
    assert client.post('/api/resource',json={'mode':'unsafe-mode'}).status_code==422


def test_existing_schema_v2_migrates_non_destructively(tmp_path,monkeypatch):
    from app import config
    monkeypatch.setattr(config,'DATA_DIR',tmp_path)
    monkeypatch.setattr(config,'DB_PATH',tmp_path/'legacy.sqlite3')
    # Construct the minimum legacy v2 records to verify migration doesn't reset data.
    with sqlite3.connect(config.DB_PATH) as con:
        con.executescript('''
          CREATE TABLE sessions (id TEXT PRIMARY KEY, title TEXT NOT NULL, created REAL NOT NULL, updated REAL NOT NULL);
          CREATE TABLE turns (id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE, question TEXT NOT NULL, answer TEXT NOT NULL, mode TEXT NOT NULL, provider TEXT NOT NULL, elapsed_ms INTEGER NOT NULL, created REAL NOT NULL);
          CREATE TABLE documents (id TEXT PRIMARY KEY, filename TEXT NOT NULL, content TEXT NOT NULL, created REAL NOT NULL);
          CREATE TABLE assessments (id TEXT PRIMARY KEY, title TEXT NOT NULL, questions_json TEXT NOT NULL, duration_seconds INTEGER NOT NULL, created REAL NOT NULL);
          CREATE TABLE attempts (id TEXT PRIMARY KEY, assessment_id TEXT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE, answers_json TEXT NOT NULL, started REAL NOT NULL, finished REAL, result_json TEXT);
          INSERT INTO sessions VALUES('legacy','Original practice',1,2);
          PRAGMA user_version=2;
        ''')
    db.initialize()
    assert db.sessions()[0]['title']=='Original practice'
    with db.connect() as con:
        assert con.execute('PRAGMA user_version').fetchone()[0]==5
        assert con.execute("SELECT name FROM sqlite_master WHERE name='assessment_drafts'").fetchone()
        assert con.execute("SELECT name FROM sqlite_master WHERE name='settings'").fetchone()


def test_optional_transcriber_emits_timestamped_unknown_speaker(client,monkeypatch):
    # Audio decoding is mocked; this verifies API shape, not real STT accuracy.
    import sys,types
    from app.main import app
    class DummySegment:
        start=0.25;end=1.7;text=' Hello practice! '
    class DummyWhisper:
        def __init__(self,*args,**kwargs): pass
        def transcribe(self,path,**kwargs):
            assert Path(path).is_file()
            return iter([DummySegment()]),types.SimpleNamespace(language='en')
    monkeypatch.setitem(sys.modules,'faster_whisper',types.SimpleNamespace(WhisperModel=DummyWhisper))
    if hasattr(app.state,'stt_model'): del app.state.stt_model
    try:
        r=client.post('/api/transcribe',files={'file':('fixture.wav',b'dummy-audio-for-mock','audio/wav')})
        assert r.status_code==200, r.text
        assert r.json()['segments']==[{'start':0.25,'end':1.7,'text':'Hello practice!','speaker':'unknown'}]
    finally:
        if hasattr(app.state,'stt_model'): del app.state.stt_model
