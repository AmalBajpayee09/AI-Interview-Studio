"""v0.10: controlled contract tests and opt-in real Docker acceptance."""
import os,threading,time
import pytest
from app import code_jobs,code_runner

def wait_for_job(queue,identifier):
    end=time.monotonic()+3
    while time.monotonic()<end:
        job=queue.get(identifier)
        if job['state'] in ('finished','failed','cancelled'):return job
        time.sleep(.02)
    raise AssertionError('Execution queue did not settle')

def test_fail_closed_without_docker(client,monkeypatch):
    monkeypatch.setattr(code_runner,'docker_available',lambda:{'available':False,'reason':'unavailable'})
    r=client.post('/api/code/jobs',json={'language':'python','code':'print(42)'})
    assert r.status_code==503 and 'disabled' in str(r.json()).lower()

def test_job_cancel_contract(client,monkeypatch):
    monkeypatch.setattr(code_runner,'docker_available',lambda:{'available':True})
    started=threading.Event()
    def runner(code,language,stdin,expected,timeout,*,cancel_event=None):
        started.set();assert cancel_event.wait(2)
        return {'status':'cancelled','exit_code':None,'stdout':'','stderr':'','elapsed_ms':10}
    monkeypatch.setattr(code_runner,'run',runner)
    r=client.post('/api/code/jobs',json={'language':'python','code':'while True: pass'})
    assert r.status_code==202 and started.wait(1)
    jid=r.json()['id'];assert client.post('/api/code/jobs/'+jid+'/cancel').status_code==200
    assert wait_for_job(code_jobs.get_queue(),jid)['state']=='cancelled'

real=os.getenv('AI_STUDIO_REAL_DOCKER_TESTS')=='1'
@pytest.mark.skipif(not real,reason='Requires explicit real Docker daemon and images')
@pytest.mark.parametrize('lang,code',[
    ('python','print(42)'),
    ('javascript','console.log(42)'),
    ('cpp','#include <iostream>\nint main(){std::cout<<42<<"\\n";}'),
    ('java','public class Main {public static void main(String[] args){System.out.println(42);}}')
])
def test_real_four_languages(lang,code):
    assert code_runner.docker_available()['available']
    r=code_runner.run(code,lang,expected='42',timeout_seconds=10)
    assert r['status']=='passed' and r['matched']

@pytest.mark.skipif(not real,reason='Requires explicit real Docker daemon and images')
def test_real_isolation_errors_timeout():
    assert code_runner.docker_available()['available']
    code='import os\nprint("nonroot" if os.geteuid()!=0 else "root")\ntry:\n open("/etc/studio-test","w")\nexcept OSError:\n print("readonly")'
    assert code_runner.run(code,'python',expected='nonroot\nreadonly')['matched']
    code='import socket\ns=socket.socket();s.settimeout(1)\ntry:\n s.connect(("1.1.1.1",53));print("open")\nexcept OSError:\n print("blocked")'
    assert code_runner.run(code,'python',expected='blocked')['matched']
    err=code_runner.run('raise RuntimeError("failure")','python')
    assert err['status']=='failed' and 'RuntimeError' in err['stderr']
    with pytest.raises(code_runner.ExecutionUnavailable,match='timed out'):
        code_runner.run('while True: pass','python',timeout_seconds=1)

@pytest.mark.skipif(not real,reason='Requires explicit real Docker daemon and images')
def test_real_cancellation():
    assert code_runner.docker_available()['available']
    flag=threading.Event();out=[]
    thread=threading.Thread(target=lambda:out.append(code_runner.run('import time\ntime.sleep(100)','python',cancel_event=flag,timeout_seconds=10)))
    thread.start();time.sleep(1.5);flag.set();thread.join(10)
    assert not thread.is_alive() and out[0]['status']=='cancelled'
