"""v0.4 checks: audio pause/resume lifecycle and Docker suite test contracts.

The suite uses deterministic Docker substitutes; real Docker execution requires a
compatible installed Docker Engine and user-installed images and is not counted here.
"""
from app import audio_live, code_runner


def test_audio_pause_requires_running(client):
    r=client.post('/api/audio/pause')
    assert r.status_code == 409
    assert 'not running' in r.text


def test_audio_resume_requires_running(client):
    assert client.post('/api/audio/resume').status_code == 409


def test_audio_pause_resume_status_and_events():
    audio=audio_live.LiveAudio()
    audio._status='running'  # Test only: capture threads are not started.
    assert audio.pause()['paused'] is True
    assert audio.resume()['paused'] is False
    assert [e['kind'] for e in audio.events()] == ['capture_paused','capture_resumed']
    audio._status='idle'


def test_code_suite_rejects_empty_and_huge_cases(client):
    data={'language':'python','code':'print(1)', 'cases':[]}
    assert client.post('/api/code/test-suite',json=data).status_code==422
    data['cases']=[{'stdin':'','expected':'1'}]*13
    assert client.post('/api/code/test-suite',json=data).status_code==422


def test_code_suite_executes_separate_containers_per_case(client,monkeypatch):
    calls=[]
    def execute(code,lang,stdin,expected,timeout):
        calls.append((code,lang,stdin,expected,timeout))
        matched=stdin==expected
        return {'status':'passed' if matched else 'failed','elapsed_ms':14.1,'matched':matched,
                'exit_code':0,'stdout':stdin,'stderr':'','stdout_truncated':False,'stderr_truncated':False}
    monkeypatch.setattr(code_runner,'run',execute)
    result=client.post('/api/code/test-suite',json={'language':'python','code':'print(input())',
        'cases':[{'label':'positive','stdin':'2','expected':'2'}, {'label':'negative','stdin':'3','expected':'4'}]})
    assert result.status_code==200
    assert result.json()['passed']==1
    assert result.json()['total']==2
    assert len(calls)==2
    assert result.json()['cases'][0]['label']=='positive'


def test_code_suite_fails_closed_without_docker(client,monkeypatch):
    monkeypatch.setattr(code_runner.shutil,'which',lambda _:None)
    result=client.post('/api/code/test-suite',json={'language':'python','code':'print(1)',
        'cases':[{'stdin':'','expected':'1'}]})
    assert result.status_code==503
    assert 'Docker' in result.text


def test_bounded_events():
    audio=audio_live.LiveAudio()
    for i in range(150): audio.emit('marker',i=i)
    assert len(audio.events()) == 128
    assert audio.status()['queue_depth']==0


def test_code_draft_saves_restores_and_deletes(client):
    path='/api/code/drafts/python'
    assert client.get(path).json()['code']==''
    assert client.put(path,json={'code':'print(42)'}).status_code==200
    assert client.get(path).json()['code']=='print(42)'
    assert client.delete(path).status_code==200
    assert client.get(path).json()['code']==''

def test_code_draft_requires_nonempty_code(client):
    assert client.put('/api/code/drafts/python',json={'code':''}).status_code==422
    assert client.get('/api/code/drafts/powershell').status_code==422


def test_runner_stops_unbounded_stdout(monkeypatch):
    """Mock container CLI that floods stdout: runner must detect and stop it."""
    from app import code_runner
    monkeypatch.setattr(code_runner,'docker_available',lambda:{'available':True})
    monkeypatch.setattr(code_runner,'available_image',lambda lang:'python:3.11-alpine')
    state={'killed':False}
    class FloodProcess:
        returncode=-9
        def poll(self): return None
        def kill(self):state['killed']=True
        def wait(self,timeout):return self.returncode
    def flood_popen(command,stdin,stdout,stderr):
        stdout.write(b'x'*33000)
        stdout.flush()
        return FloodProcess()
    monkeypatch.setattr(code_runner.subprocess,'Popen',flood_popen)
    monkeypatch.setattr(code_runner.subprocess,'run',lambda *args,**kwargs:None)
    result=code_runner.run('print("x")','python')
    assert state['killed']
    assert result['status']=='failed'
    assert result['stdout_truncated']
    assert len(result['stdout'])<=32768
