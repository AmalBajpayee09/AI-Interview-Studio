"""v1.0.0-rc.3 startup security and session-continuity tests.

These use a real Python worker HTTP subprocess and controlled AI stubs, not a real Ollama
installation and not a compiled Windows desktop. Live-provider acceptance remains opt-in.
"""
import asyncio
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import pytest
import httpx
from app import config, db, providers, startup_events
from app.main import ACTIVE_GENERATIONS, get_ask_messages, AskBody


def frames(response):
    return [json.loads(x[6:]) for x in response.text.splitlines() if x.startswith('data: ')]


def test_startup_events_never_echo_input_or_auth(tmp_path, monkeypatch):
    monkeypatch.setenv('STUDIO_DIAGNOSTIC_DIR',str(tmp_path))
    monkeypatch.setenv('STUDIO_WORKER_TOKEN','TOP_SECRET_WORKER_TOKEN')
    monkeypatch.setenv('OPENAI_API_KEY','sk-test-very-private')
    startup_events.record('process_started')
    startup_events.record('database_initialized')
    content=(tmp_path/'worker-startup.jsonl').read_text()
    assert 'TOP_SECRET' not in content and 'sk-test' not in content
    assert all(set(json.loads(l))=={'timestamp_ms','component','stage','outcome'} for l in content.splitlines())


def test_startup_events_reject_untrusted_details(tmp_path, monkeypatch):
    monkeypatch.setenv('STUDIO_DIAGNOSTIC_DIR',str(tmp_path))
    with pytest.raises(ValueError): startup_events.record('My resume: secret sensitive text')
    with pytest.raises(ValueError): startup_events.record('worker_stopping','key=secret')
    assert not list(tmp_path.iterdir())


def test_startup_log_rotates_without_unbounded_growth(tmp_path,monkeypatch):
    monkeypatch.setenv('STUDIO_DIAGNOSTIC_DIR',str(tmp_path))
    path=tmp_path/'worker-startup.jsonl'
    path.write_text('x'*(startup_events.MAX_SIZE+1))
    startup_events.record('database_initialized')
    assert path.stat().st_size<200 and (tmp_path/'worker-startup.previous.jsonl').exists()


def test_followup_context_and_order_recovered_after_db_reopen(client,monkeypatch):
    class ContextAware:
        inputs=[]
        async def stream(self,messages,model):
            self.inputs.append(messages)
            yield 'verified mock transcript NOT live Ollama'
    model=ContextAware()
    monkeypatch.setattr(providers,'get_provider',lambda _: (model,'stub'))
    sid=client.post('/api/sessions',json={'title':'A multi-step practice session'}).json()['id']
    for q in ['Explain a Python stack','What changes if it must be thread-safe?']:
        assert frames(client.post('/api/ask/stream',json={'session_id':sid,'question':q}))[-1]['type']=='done'
    assert 'Python stack' in str(model.inputs[1])
    assert 'verified mock' in str(model.inputs[1])
    db.initialize() # same on-disk SQLite database, as in process restart
    restored=client.get(f'/api/sessions/{sid}/turns').json()
    assert [turn['question'] for turn in restored]==['Explain a Python stack','What changes if it must be thread-safe?']
    assert len(restored)==2 and all(turn['answer'] for turn in restored)
    assert sid in [s['id'] for s in client.get('/api/sessions').json()]


def test_cancel_then_retry_does_not_duplicate_or_save_partial(client,monkeypatch):
    sid=client.post('/api/sessions').json()['id']
    class Interrupted:
        async def stream(self,messages,model):
            yield 'uncommitted partial'
            ACTIVE_GENERATIONS.pop(sid,None)
            yield 'never saved'
    monkeypatch.setattr(providers,'get_provider',lambda _: (Interrupted(),'stub'))
    assert frames(client.post('/api/ask/stream',json={'session_id':sid,'question':'Retry context'}))[-1]['type']=='error'
    assert client.get(f'/api/sessions/{sid}/turns').json()==[]
    class Recovered:
        async def stream(self,messages,model): yield 'valid full answer'
    monkeypatch.setattr(providers,'get_provider',lambda _: (Recovered(),'stub'))
    assert frames(client.post('/api/ask/stream',json={'session_id':sid,'question':'Retry context'}))[-1]['type']=='done'
    assert len(client.get(f'/api/sessions/{sid}/turns').json())==1


def test_real_subprocess_auth_database_and_restart(tmp_path):
    """End-to-end real HTTP/SQLite and worker lifecycle; AI generation is NOT exercised."""
    with socket.socket() as listener:
        listener.bind(('127.0.0.1',0));port=listener.getsockname()[1]
    token='local_test_token_'+'x'*24
    env={**os.environ,'STUDIO_PORT':str(port),'STUDIO_WORKER_TOKEN':token,
         'STUDIO_DATA_DIR':str(tmp_path/'state'),'STUDIO_DIAGNOSTIC_DIR':str(tmp_path/'logs'),
         'PYTHONPATH':str(Path(__file__).resolve().parents[1])}
    exe=Path(__file__).resolve().parents[1]/'run_worker.py'
    url=f'http://127.0.0.1:{port}'
    sid=None
    for attempt in range(2):
        with subprocess.Popen([sys.executable,str(exe)],env=env,stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL) as process:
            try:
                with httpx.Client(timeout=0.4) as http:
                    start=time.monotonic()
                    while True:
                        if process.poll() is not None: raise AssertionError('Worker exited before readiness')
                        try:
                            res=http.get(url+'/api/health',headers={'X-Studio-Token':token})
                            if res.status_code==200 and res.json()['version']=='1.0.0-rc.3': break
                        except httpx.HTTPError: pass
                        if time.monotonic()-start>12: raise AssertionError('Worker did not authenticate in time')
                        time.sleep(0.08)
                    assert http.get(url+'/api/health').status_code==401
                    assert http.get(url+'/api/health',headers={'X-Studio-Token':'wrong'}).status_code==401
                    headers={'X-Studio-Token':token}
                    if attempt==0:
                        sid=http.post(url+'/api/sessions',json={'title':'Recovery test'},headers=headers).json()['id']
                    else:
                        sessions=http.get(url+'/api/sessions',headers=headers).json()
                        assert sid in [session['id'] for session in sessions]
                        assert http.get(url+f'/api/sessions/{sid}/turns',headers=headers).json()==[]
            finally:
                process.terminate()
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
    events=(tmp_path/'logs'/'worker-startup.jsonl').read_text()
    assert 'database_initialized' in events
    assert token not in events
    assert (tmp_path/'state'/'studio.sqlite3').is_file()


@pytest.mark.skipif(os.getenv('STUDIO_LIVE_OLLAMA_TEST')!='1',reason='requires genuine running Ollama and pulled model')
def test_real_ollama_api_stream_and_followup(tmp_path,monkeypatch):
    """Real local Ollama model via the actual HTTP API, never MockTransport."""
    from fastapi.testclient import TestClient
    from app.main import app
    available=asyncio.run(providers.list_local_models())
    assert available['online'] and available['models'], 'Ollama must be running with a model pulled'
    name=os.environ.get('STUDIO_TEST_OLLAMA_MODEL') or available['models'][0]
    assert name in available['models']
    monkeypatch.setattr(config,'DATA_DIR',tmp_path)
    monkeypatch.setattr(config,'DB_PATH',tmp_path/'real-model.sqlite3')
    with TestClient(app) as client:
        sid=client.post('/api/sessions',json={'title':'Live local model acceptance'}).json()['id']
        first=frames(client.post('/api/ask/stream',json={
            'session_id':sid,'question':'Explain a stack data structure in one sentence.',
            'provider':'ollama','model':name}))
        assert first[-1]['type']=='done',first[-1]
        assert any(f['type']=='token' for f in first)
        second=frames(client.post('/api/ask/stream',json={
            'session_id':sid,'question':'Name one real-world use of the same structure.',
            'provider':'ollama','model':name}))
        assert second[-1]['type']=='done',second[-1]
        assert len(client.get(f'/api/sessions/{sid}/turns').json())==2
        db.initialize()
        assert len(client.get(f'/api/sessions/{sid}/turns').json())==2
