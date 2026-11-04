"""v0.5 end-to-end backend checks. No hardware or cloud integration is implied."""
from __future__ import annotations
import math
import sqlite3
import time
from app import db,logic


def custom_questions():
    return [
        {'id':'single','stem':'Which is FIFO?','kind':'single','options':[{'label':'A','text':'Stack'},{'label':'B','text':'Queue'}],'correct':'B','section':'DSA'},
        {'id':'multi','stem':'Select even numbers','kind':'multiple','options':[{'label':'A','text':'2'},{'label':'B','text':'3'},{'label':'C','text':'4'}],'correct':['A','C'],'section':'Aptitude','points':2},
        {'id':'numeric','stem':'2 + 2','kind':'numerical','correct':4,'tolerance':0.01,'section':'Aptitude','points':3},
    ]


def test_multi_numeric_assessment_end_to_end(client):
    q=custom_questions()
    r=client.post('/api/assessments',json={'title':'Mixed practice','duration_seconds':180,'questions':q})
    assert r.status_code==200,r.text
    aid=r.json()['id']
    listing=client.get('/api/assessments').json()
    saved=next(a for a in listing if a['id']==aid)['questions']
    assert saved[1]['kind']=='multiple' and saved[2]['kind']=='numerical'
    assert 'correct' not in saved[1] and 'correct' not in saved[2]
    started=time.time()
    draft={'answers':{'single':'B','multi':['A','C'],'numeric':'4.005'},'review':['numeric'],'started':started}
    assert client.post(f'/api/assessments/{aid}/draft',json=draft).status_code==200
    assert client.get(f'/api/assessments/{aid}/draft').json()['draft']['answers']['multi']==['A','C']
    result=client.post(f'/api/assessments/{aid}/submit',json={'answers':draft['answers'],'started':started}).json()
    assert (result['correct'],result['incorrect'],result['unanswered'])==(3,0,0)
    assert result['score']==6 and result['maximum']==6
    assert result['sections']['Aptitude']['correct']==2
    assert client.get(f'/api/assessments/{aid}/draft').json()['draft'] is None


def test_mixed_scoring_negative_and_missing():
    q=custom_questions()
    result=logic.score(q,{'single':'A','multi':[],'numeric':'4.25'},negative_marking=.25)
    assert (result['correct'],result['incorrect'],result['unanswered'])==(0,2,1)
    assert result['score']==-1 and result['sections']['Aptitude']['unanswered']==1
    assert result['sections']['DSA']['score']==-.25


def test_nonfinite_numeric_inputs_and_bad_quiz_rejected(client):
    q=custom_questions()
    for invalid in ('NaN','Infinity','-Infinity'):
        bad=[dict(q[-1],correct=invalid)]
        assert client.post('/api/assessments',json={'title':'Invalid','duration_seconds':180,'questions':bad}).status_code in (400,422)
    assert logic.score([q[-1]],{'numeric':'NaN'})['incorrect']==1
    for field in ['tolerance','points']:
        bad=[dict(q[-1],**{field:'Infinity'})]
        assert client.post('/api/assessments',json={'title':'Invalid','duration_seconds':180,'questions':bad}).status_code in (400,422)


def test_transcript_opt_in_storage_and_session_isolation(client):
    a=client.post('/api/sessions',json={'title':'A'}).json()['id']
    b=client.post('/api/sessions',json={'title':'B'}).json()['id']
    assert client.get(f'/api/sessions/{a}/transcripts').json()['transcripts']==[]
    payload={'text':'Explain ACID transactions','source_id':'microphone-1','speaker':'unknown','language':'en','started_at':12.5,'ended_at':14.1}
    r=client.post(f'/api/sessions/{a}/transcripts',json=payload)
    assert r.status_code==200, r.text
    stored=client.get(f'/api/sessions/{a}/transcripts').json()['transcripts']
    assert stored[0]['text']==payload['text'] and stored[0]['speaker']=='unknown'
    assert client.get(f'/api/sessions/{b}/transcripts').json()['transcripts']==[]
    db.initialize()
    assert client.get(f'/api/sessions/{a}/transcripts').json()['transcripts'][0]['text']==payload['text']
    assert len(client.get('/api/export').json()['transcripts'][a])==1
    assert client.delete(f'/api/sessions/{a}/transcripts').json()['deleted']==1
    assert client.get(f'/api/sessions/{a}/transcripts').json()['transcripts']==[]


def test_transcript_invalid_and_unknown_session(client):
    sid=client.post('/api/sessions').json()['id']
    path=f'/api/sessions/{sid}/transcripts'
    assert client.post(path,json={'text':'','source_id':'mic'}).status_code==422
    assert client.post(path,json={'text':'Hi','source_id':'mic','speaker':'candidate','speaker_confidence':1.5}).status_code==422
    assert client.post(path,json={'text':'Hi','source_id':'mic','started_at':10,'ended_at':5}).status_code==400
    assert client.post('/api/sessions/missing/transcripts',json={'text':'Hi','source_id':'mic'}).status_code==404
    assert client.get('/api/sessions/missing/transcripts').status_code==404


def test_transcript_context_is_session_scoped(client,monkeypatch):
    from app import providers
    a=client.post('/api/sessions').json()['id']
    b=client.post('/api/sessions').json()['id']
    client.post(f'/api/sessions/{a}/transcripts',json={'text':'I designed a one-of-a-kind purple queue','source_id':'mic'})
    received=[]
    class CaptureProvider:
        async def stream(self,messages,model):
            received.append('\\n'.join(x['content'] for x in messages))
            yield 'Sample explanation'
    monkeypatch.setattr(providers,'get_provider',lambda provider: (CaptureProvider(),'mock-model'))
    for sid in (a,b):
        resp=client.post('/api/ask/stream',json={'session_id':sid,'question':'Explain a data structure'})
        assert '"type": "done"' in resp.text
    assert 'purple queue' in received[0]
    assert 'purple queue' not in received[1]


def test_transcript_deletion_cascades_with_session(client):
    sid=client.post('/api/sessions').json()['id']
    client.post(f'/api/sessions/{sid}/transcripts',json={'text':'no raw audio is stored','source_id':'mic'})
    client.delete(f'/api/sessions/{sid}')
    with db.connect() as cx:
        assert cx.execute('SELECT COUNT(*) FROM transcript_segments').fetchone()[0]==0
        assert cx.execute('PRAGMA user_version').fetchone()[0]==7


def test_existing_schema_v4_upgrades_without_data_loss(client):
    sid=client.post('/api/sessions',json={'title':'Keep this'}).json()['id']
    with db.connect() as cx:
        cx.execute('DROP TABLE transcript_segments')
        cx.execute('PRAGMA user_version=4')
    db.initialize()
    assert db.get_turns(sid)==[]
    assert db.sessions()[0]['title']=='Keep this'
    with db.connect() as cx:
        assert cx.execute('PRAGMA user_version').fetchone()[0]==7
        assert cx.execute("SELECT name FROM sqlite_master WHERE name='transcript_segments'").fetchone() is not None


def test_transcript_database_backup(client,tmp_path):
    sid=client.post('/api/sessions').json()['id']
    client.post(f'/api/sessions/{sid}/transcripts',json={'text':'Review joins','source_id':'mic'})
    content=client.get('/api/backup/database').content
    dest=tmp_path/'saved.sqlite3';dest.write_bytes(content)
    with sqlite3.connect(dest) as con:
        assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert con.execute('SELECT text FROM transcript_segments').fetchone()[0]=='Review joins'
