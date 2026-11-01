from app import logic,db

def test_classification():
    assert logic.classify('Implement a binary search function')=='coding'
    assert logic.classify('What is FIFO?\nA) queue\nB) stack')=='mcq'

def test_segment():
    assert len(logic.segment('What is SQL? Explain joins?'))==2

def test_scoring():
    q=[{'id':'one','correct':'A'},{'id':'two','correct':['A','C']},{'id':'three','correct':'B'}]
    result=logic.score(q,{'one':'A','two':['A','C'],'three':'A'})
    assert result['score']==1.75 and result['correct']==2 and result['incorrect']==1

def test_syntax_safety():
    assert logic.syntax_check('def f(x): return x') ['status']=='parsed'
    assert logic.syntax_check('def invalid(:')['status']=='syntax_error'
    assert logic.syntax_check('console.log(1)','javascript')['status']=='unavailable'

def test_sessions_recovery(client):
    s=client.post('/api/sessions',json={'title':'Test'}).json()
    assert s['id']
    db.save_turn(s['id'],'Hi','Hello','short','ollama',25)
    assert len(client.get(f"/api/sessions/{s['id']}/turns").json())==1
    assert client.get('/api/sessions').json()[0]['title']=='Test'
    assert client.delete(f"/api/sessions/{s['id']}").json()['deleted'] is True
    assert client.get(f"/api/sessions/{s['id']}/turns").status_code==404

def test_assessment(client):
    a=client.get('/api/assessments').json()[0]
    assert 'correct' not in a['questions'][0]
    import time
    result=client.post(f"/api/assessments/{a['id']}/submit",json={'answers':{'q1':'B','q2':'C'},'started':time.time()}).json()
    assert result['correct']==2 and result['unanswered']==2
    assert client.get('/api/stats').json()['assessments_completed']==1

def test_parse_upload_documents(client):
    r=client.post('/api/files/extract',files={'file':('notes.txt',b'My project uses RAG','text/plain')})
    assert r.status_code==200
    d=client.post('/api/documents',json={'filename':'notes.txt','content':r.json()['text']}).json()
    assert len(client.get('/api/documents').json())==1
    assert client.delete('/api/documents/'+d['id']).json()['deleted']

def test_cloud_opt_in(client):
    import os
    s=client.post('/api/sessions').json()
    r=client.post('/api/ask/stream',json={'session_id':s['id'],'question':'Explain SQL','provider':'cloud'})
    assert 'Cloud disabled' in r.text

def test_origin_restriction(client):
    assert client.get('/api/health',headers={'Origin':'https://evil.example'}).status_code==403

def test_diagnostics(client):
    data=client.get('/api/diagnostics').json()
    assert data['memory_total_gb']>0 and data['cpu_count']>0

def test_communication(client):
    x=client.post('/api/communication/feedback',json={'transcript':'um hello world','seconds':2}).json()
    assert x['words']==3 and x['wpm']==90


def test_no_correct_answers_leaked(client):
    response=client.get('/api/assessments')
    assert 'questions_json' not in response.text
    assert '"correct"' not in response.text
    assert '"explanation"' not in response.text

def test_companion_page_served(client):
    r=client.get('/')
    assert r.status_code==200 and 'AI INTERVIEW' in r.text

def test_fake_stream_persists(client,monkeypatch):
    from app import providers
    class FakeProvider:
        async def stream(self,messages,model):
            assert messages[-1]['content']=='What is an index?'
            yield 'An index ' 
            yield 'accelerates lookup.'
    monkeypatch.setattr(providers,'get_provider',lambda name: (FakeProvider(),'test-model'))
    s=client.post('/api/sessions').json()
    r=client.post('/api/ask/stream',json={'session_id':s['id'],'question':'What is an index?'})
    assert r.status_code==200 and '"type": "done"' in r.text
    turns=client.get(f"/api/sessions/{s['id']}/turns").json()
    assert turns[0]['answer']=='An index accelerates lookup.'

def test_unexpected_file_type(client):
    r=client.post('/api/files/extract',files={'file':('x.exe',b'123','application/octet-stream')})
    assert r.status_code==415

def test_unknown_ask_session(client):
    assert client.post('/api/ask/stream',json={'session_id':'missing','question':'What is SQL?'}).status_code==404

def test_companion_origin_for_post(client):
    r=client.post('/api/sessions',json={'title':'same-origin'},headers={'Origin':'http://127.0.0.1:8765'})
    assert r.status_code==200


def test_user_export_includes_document_content(client):
    client.post('/api/documents',json={'filename':'resume.txt','content':'Experience with SQL and Python'})
    result=client.get('/api/export').json()
    assert 'Experience with SQL' in result['documents'][0]['content']
