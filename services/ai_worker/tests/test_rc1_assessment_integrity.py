"""Release-candidate API/SQLite regression; not Windows desktop or proctoring acceptance."""
import sqlite3
import time
from app import db


def strict_quiz(client):
    response=client.post('/api/assessments',json={
        'title':'Strict timed practice','duration_seconds':120,
        'require_start':True,'negative_marking':0.5,'cutoff_pct':75,
        'questions':[
            {'id':'a','stem':'First','kind':'single','correct':'B',
             'options':[{'label':'A','text':'Wrong'},{'label':'B','text':'Right'}]},
            {'id':'b','stem':'Second','kind':'single','correct':'A',
             'options':[{'label':'A','text':'Right'},{'label':'B','text':'Wrong'}]}]})
    assert response.status_code==200,response.text
    return response.json()['id']


def test_strict_start_and_no_clock_reset(client):
    aid=strict_quiz(client);url=f'/api/assessments/{aid}'
    stamp=time.time()
    assert client.post(url+'/submit',json={'started':stamp,'answers':{'a':'B'}}).status_code==409
    assert client.post(url+'/draft',json={'started':stamp,'answers':{'a':'B'}}).status_code==409
    assert client.delete(url+'/draft').status_code==409
    at=client.post(url+'/start').json()['draft']['started']
    assert client.post(url+'/draft',json={'started':at-60,'answers':{'a':'B'}}).status_code==409
    assert client.post(url+'/draft',json={'started':at,'answers':{'a':'B'}}).status_code==200
    assert client.post(url+'/start').json()['draft']['started']==at
    assert client.delete(url+'/draft').status_code==409


def test_server_grading_policy_cutoff_and_retry(client):
    aid=strict_quiz(client)
    listing=next(x for x in client.get('/api/assessments').json() if x['id']==aid)
    assert listing['require_start']==1 and listing['negative_marking']==.5
    assert all('correct' not in q for q in listing['questions'])
    at=client.post(f'/api/assessments/{aid}/start').json()['draft']['started']
    first=client.post(f'/api/assessments/{aid}/submit',json={
        'started':at,'answers':{'a':'B','b':'B'},'negative_marking':0})
    assert first.status_code==200,first.text
    data=first.json()
    assert data['score']==.5 and data['negative_marking']==.5
    assert data['passed_cutoff'] is False and data['cutoff_pct']==75
    assert client.get(f'/api/assessments/{aid}/draft').json()['draft'] is None
    assert client.post(f'/api/assessments/{aid}/draft',json={
        'started':at,'answers':{'a':'B','b':'A'}}).status_code==409
    retry=client.post(f'/api/assessments/{aid}/submit',json={
        'started':at,'answers':{'a':'B','b':'A'}})
    assert retry.status_code==200 and retry.json()['duplicate_submission']
    assert retry.json()['attempt_id']==data['attempt_id']
    assert retry.json()['score']==data['score']
    with db.connect() as conn:
        assert conn.execute('SELECT count(*) FROM attempts WHERE assessment_id=?',(aid,)).fetchone()[0]==1


def test_expired_attempt_scores_saved_answers_only(client):
    aid=strict_quiz(client);url=f'/api/assessments/{aid}'
    at=client.post(url+'/start').json()['draft']['started']
    assert client.post(url+'/draft',json={'started':at,'answers':{'a':'B'}}).status_code==200
    expired=time.time()-150
    with db.connect() as conn:
        conn.execute('UPDATE assessment_drafts SET started=? WHERE assessment_id=?',(expired,aid))
    result=client.post(url+'/submit',json={'started':expired,
        'answers':{'a':'B','b':'A'},'negative_marking':0})
    assert result.status_code==200,result.text
    data=result.json()
    assert data['timed_out'] is True and data['correct']==1 and data['unanswered']==1
    assert data['score']==1 and data['passed_cutoff'] is False


def test_v6_schema_upgrade_preserves_legacy_practice(client,tmp_path,monkeypatch):
    from app import config
    filename=tmp_path/'old.sqlite3'
    with sqlite3.connect(filename) as conn:
        conn.executescript("""
            CREATE TABLE assessments(id TEXT PRIMARY KEY,title TEXT NOT NULL,
                questions_json TEXT NOT NULL,duration_seconds INTEGER NOT NULL,created REAL NOT NULL);
            CREATE TABLE sessions(id TEXT PRIMARY KEY,title TEXT NOT NULL,created REAL NOT NULL,updated REAL NOT NULL);
            CREATE TABLE attempts(id TEXT PRIMARY KEY,assessment_id TEXT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
                answers_json TEXT NOT NULL,started REAL NOT NULL,finished REAL,result_json TEXT);
            CREATE TABLE attempt_receipts(assessment_id TEXT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
                started REAL NOT NULL,attempt_id TEXT NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
                PRIMARY KEY(assessment_id,started));
            CREATE TABLE assessment_drafts(assessment_id TEXT PRIMARY KEY REFERENCES assessments(id) ON DELETE CASCADE,
                answers_json TEXT NOT NULL,review_json TEXT NOT NULL,started REAL NOT NULL,updated REAL NOT NULL);
            PRAGMA user_version=6;
        """)
        conn.execute('INSERT INTO assessments VALUES(?,?,?,?,?)',
                     ('legacy','Old exercise','[{"id":"q","stem":"Q","correct":"A","kind":"single","options":[{"label":"A","text":"Yes"}]}]',120,time.time()))
        conn.execute('INSERT INTO sessions VALUES(?,?,?,?)',('old-session','Preserved',time.time(),time.time()))
    monkeypatch.setattr(config,'DB_PATH',filename)
    db.initialize()
    with db.connect() as conn:
        assert conn.execute('PRAGMA user_version').fetchone()[0]==7
        assert conn.execute('SELECT id FROM sessions WHERE id=?',('old-session',)).fetchone()
        policy=conn.execute('SELECT require_start,negative_marking,cutoff_pct FROM assessments WHERE id=?',('legacy',)).fetchone()
        assert policy['require_start']==0 and policy['negative_marking']==.25 and policy['cutoff_pct'] is None
    response=client.post('/api/assessments/legacy/submit',json={'started':time.time(),'answers':{}})
    assert response.status_code==200,response.text
    assert response.json()['timing_enforcement']=='legacy_unstarted_practice'
