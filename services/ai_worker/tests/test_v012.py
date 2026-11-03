"""v0.12 server start, autosave recovery and idempotent final submission."""
from app import db,logic

def create_quiz(client):
    r=client.post('/api/assessments',json={'title':'Recovery check','duration_seconds':120,
       'questions':[{'id':'n','kind':'numerical','stem':'Compute','correct':'42','tolerance':0.1},
                    {'id':'s','kind':'single','stem':'Choice','options':[{'label':'A','text':'yes'},{'label':'B','text':'no'}],'correct':'A'}]})
    assert r.status_code==200
    return r.json()['id']

def test_start_recover_and_duplicate(client):
    aid=create_quiz(client)
    r=client.post(f'/api/assessments/{aid}/start');assert r.status_code==200
    first=r.json()['draft'];assert not first['recovered']
    assert client.post(f'/api/assessments/{aid}/draft',json={'answers':{'n':'42'},'review':['n'],'started':first['started']}).status_code==200
    restored=client.post(f'/api/assessments/{aid}/start').json()['draft']
    assert restored['recovered'] and restored['answers']=={'n':'42'} and restored['started']==first['started']
    body={'answers':{'n':'42','s':'A'},'started':first['started'],'negative_marking':.25}
    original=client.post(f'/api/assessments/{aid}/submit',json=body)
    assert original.status_code==200 and original.json()['correct']==2 and not original.json()['duplicate_submission']
    retry=client.post(f'/api/assessments/{aid}/submit',json=body)
    assert retry.status_code==200 and retry.json()['duplicate_submission']
    assert original.json()['attempt_id']==retry.json()['attempt_id']
    with db.connect() as d:
        assert d.execute('SELECT count(*) FROM attempts WHERE assessment_id=?',(aid,)).fetchone()[0]==1

def test_v5_migration_keeps_old_rows(client):
    aid=create_quiz(client)
    old=db.save_attempt(aid,{},logic.score([],{}),1000)
    session=db.session_create('Keep session')
    with db.connect() as d:
        d.execute('DROP TABLE IF EXISTS attempt_receipts')
        d.execute('PRAGMA user_version=5')
    db.initialize()
    with db.connect() as d:
        assert d.execute('PRAGMA user_version').fetchone()[0]>=6
        assert d.execute('SELECT id FROM attempts WHERE id=?',(old,)).fetchone()
        assert d.execute('SELECT id FROM sessions WHERE id=?',(session['id'],)).fetchone()
