"""Real subprocess/HTTP/SQLite continuity smoke. No mocked provider or Windows WebView claims."""
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import httpx

WORKER=Path(__file__).resolve().parents[1]/'services'/'ai_worker'/'run_worker.py'

def run():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    base=f'http://127.0.0.1:{port}'
    token=secrets.token_urlsafe(36)
    checks=[]
    with tempfile.TemporaryDirectory(prefix='studio-rc1-') as tmp:
        env={**os.environ,'STUDIO_PORT':str(port),'STUDIO_WORKER_TOKEN':token,
             'STUDIO_DATA_DIR':str(Path(tmp)/'data'),
             'STUDIO_DIAGNOSTIC_DIR':str(Path(tmp)/'logs'),
             'PYTHONPATH':str(WORKER.parent)}
        aid=None;start=None
        for cycle in (0,1):
            proc=subprocess.Popen([sys.executable,str(WORKER)],env=env,
                                  stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            try:
                with httpx.Client(timeout=1.5) as client:
                    clock=time.monotonic()
                    while time.monotonic()-clock<18:
                        if proc.poll() is not None: raise AssertionError('Worker exited before readiness')
                        try:
                            health=client.get(base+'/api/health',headers={'X-Studio-Token':token})
                            if health.status_code==200 and health.json().get('status')=='ok':break
                        except httpx.HTTPError:pass
                        time.sleep(.075)
                    else: raise AssertionError('Worker readiness timeout')
                    assert client.get(base+'/api/health').status_code==401
                    assert client.get(base+'/api/health',headers={'X-Studio-Token':'incorrect'}).status_code==401
                    h={'X-Studio-Token':token}
                    if cycle==0:
                        question={'id':'a','stem':'Choice','kind':'single','correct':'B',
                                  'options':[{'label':'A','text':'Wrong'},{'label':'B','text':'Right'}]}
                        exam={'title':'Worker restart acceptance','duration_seconds':120,'require_start':True,
                              'negative_marking':0.5,'cutoff_pct':75,'questions':[question]}
                        reply=client.post(base+'/api/assessments',headers=h,json=exam)
                        assert reply.status_code==200,reply.text
                        aid=reply.json()['id']
                        draft=client.post(base+f'/api/assessments/{aid}/start',headers=h).json()['draft']
                        start=draft['started']
                        saved=client.post(base+f'/api/assessments/{aid}/draft',headers=h,
                                          json={'started':start,'answers':{'a':'B'},'review':[]})
                        assert saved.status_code==200,saved.text
                        checks.append('authenticated_start_and_autosave')
                    else:
                        restored=client.post(base+f'/api/assessments/{aid}/start',headers=h).json()['draft']
                        assert restored['started']==start and restored['answers']=={'a':'B'}
                        submitted={'started':start,'answers':{'a':'B'},'negative_marking':0}
                        done=client.post(base+f'/api/assessments/{aid}/submit',headers=h,json=submitted)
                        assert done.status_code==200,done.text
                        first=done.json()
                        assert first['score']==1 and first['negative_marking']==.5
                        assert first['passed_cutoff'] is True
                        retry=client.post(base+f'/api/assessments/{aid}/submit',headers=h,json=submitted)
                        assert retry.json()['duplicate_submission']
                        assert first['attempt_id']==retry.json()['attempt_id']
                        checks.append('sqlite_draft_restore_and_atomic_receipt')
            finally:
                proc.terminate()
                try:proc.wait(timeout=5)
                except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=5)
        diagnostics=(Path(tmp)/'logs'/'worker-startup.jsonl').read_text()
        assert 'database_initialized' in diagnostics and token not in diagnostics
        checks.append('no_token_in_diagnostics')
    return {'result':'PASS','checks':checks,
            'not_tested':['Windows installed UI','real Ollama','Windows Docker Desktop','Windows audio','installer upgrade']}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
