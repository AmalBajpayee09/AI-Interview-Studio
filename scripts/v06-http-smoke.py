"""Localhost real-socket security + API smoke. Does NOT validate live AI providers."""
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import httpx

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='studio-v06-smoke-') as root:
    env=os.environ.copy()
    env.update(STUDIO_DATA_DIR=root, STUDIO_WORKER_TOKEN='local-only-smoke-token-123',PYTHONPATH=str(ROOT/'services/ai_worker'))
    with socket.socket() as s:
        s.bind(('127.0.0.1',0))
        port=s.getsockname()[1]
    server=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(port),'--log-level','error'],cwd=str(ROOT/'services/ai_worker'),env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    results=[]
    try:
        base=f'http://127.0.0.1:{port}'
        for _ in range(60):
            try:
                if httpx.get(base+'/api/health',timeout=0.3).status_code==401: break
            except httpx.HTTPError: time.sleep(0.05)
        else: raise RuntimeError('worker did not become ready')
        with httpx.Client(base_url=base,headers={'X-Studio-Token':env['STUDIO_WORKER_TOKEN']},timeout=5.0) as cli:
            def check(label,ok,details=''):
                results.append(dict(name=label,pass_status=bool(ok),details=details))
                if not ok:raise AssertionError(label+': '+details)
            check('unauthenticated request rejected',httpx.get(base+'/api/health').status_code==401)
            check('origin restriction',cli.get('/api/health',headers={'Origin':'https://unknown.invalid'}).status_code==403)
            check('worker health',cli.get('/api/health').json()['version']=='0.6.0')
            check('Windows-only credential storage fails closed',cli.post('/api/cloud/credential',json={'api_key':'sk-local-smoke-test-12345'}).status_code==503 if sys.platform!='win32' else True,'Linux-specific test')
            check('cloud privacy default',cli.get('/api/cloud/status').json()['consent'] is False)
            check('cloud consent enables explicitly',cli.post('/api/cloud/consent',json={'enabled':True}).json()['consent'] is True)
            check('cloud consent disable',cli.post('/api/cloud/consent',json={'enabled':False}).json()['consent'] is False)
            sid=cli.post('/api/sessions',json={'title':'Smoke test'}).json()['id']
            check('persistent session created',len(cli.get('/api/sessions').json())==1)
            check('AI usage initially empty',cli.get('/api/ai/usage').json()['entries']==[])
            check('SQL read-only query',cli.post('/api/sql/query',json={'query':'SELECT COUNT(*) AS n FROM employees'}).status_code==200)
            check('SQL write blocked',cli.post('/api/sql/query',json={'query':'DROP TABLE employees'}).status_code==400)
            check('nonexistent AI usage 404',cli.get('/api/sessions/missing/ai/usage').status_code==404)
            check('cancellation endpoint idempotent',cli.post(f'/api/ask/{sid}/cancel').json()['cancelled'] is False)
            check('delete session',cli.delete(f'/api/sessions/{sid}').json()['deleted'] is True)
            measurements=[]
            for _ in range(30):
                t=time.perf_counter()
                r=cli.get('/api/health')
                if r.status_code==200: measurements.append((time.perf_counter()-t)*1000)
            sorted_ms=sorted(measurements)
        report={'version':'0.6.0','environment':sys.platform,'test_type':'real localhost HTTP, not desktop or live AI','checks':results,'pass_count':sum(v['pass_status'] for v in results),'total_count':len(results),'health_p50_ms':round(sorted_ms[len(sorted_ms)//2],3),'health_p95_ms':round(sorted_ms[int(len(sorted_ms)*0.95)-1],3),'health_samples':len(sorted_ms)}
        (ROOT/'docs/V06_HTTP_SMOKE.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:report[k] for k in ['pass_count','total_count','health_p50_ms','health_p95_ms','health_samples']}))
    finally:
        server.terminate()
        try:server.wait(timeout=4)
        except subprocess.TimeoutExpired:server.kill();server.wait()
