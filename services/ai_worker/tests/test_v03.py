"""v0.3 regression tests (Docker execution is mocked unless real images are installed)."""
import os
import subprocess
import types
import pytest
from app import code_runner


def test_worker_token_required(client, monkeypatch):
    monkeypatch.setenv('STUDIO_WORKER_TOKEN','a'*64)
    assert client.get('/api/health').status_code==401
    assert client.get('/api/health',headers={'X-Studio-Token':'bad'}).status_code==401
    response=client.get('/api/health',headers={'X-Studio-Token':'a'*64})
    assert response.status_code==200
    assert response.json()['version']=='0.5.0'


def test_code_runner_unavailable_never_runs(client,monkeypatch):
    monkeypatch.setattr(code_runner.shutil,'which',lambda name:None)
    r=client.post('/api/code/execute',json={'language':'python','code':'print(1)'})
    assert r.status_code==503
    assert 'Docker CLI not installed' in r.text
    assert client.get('/api/code/capabilities').json()['available'] is False


def test_code_runner_inputs_are_validated(monkeypatch):
    monkeypatch.setattr(code_runner.shutil,'which',lambda name: None)
    with pytest.raises(code_runner.InvalidCode): code_runner.run('', 'python')
    with pytest.raises(code_runner.InvalidCode): code_runner.run('print(1)','powershell')
    with pytest.raises(code_runner.InvalidCode): code_runner.run('print(1)','python',stdin='x'*17000)


def test_docker_command_enforces_isolation(monkeypatch):
    monkeypatch.setattr(code_runner,'docker_available',lambda: {'available':True})
    monkeypatch.setattr(code_runner,'available_image',lambda lang: 'python:3.11-alpine')
    calls=[]
    class FakeProcess:
        returncode=0
        def poll(self): return 0
        def wait(self,timeout): return 0
    def fake_popen(command,stdin,stdout,stderr):
        calls.append(command)
        stdout.write(b'42\n')
        stdout.flush()
        return FakeProcess()
    monkeypatch.setattr(code_runner.subprocess,'Popen',fake_popen)
    result=code_runner.run('print(42)', 'python', expected='42')
    assert result['status']=='passed' and result['matched']
    cmd=calls[-1]
    for flag in ('--network','none','--read-only','--cap-drop','ALL','--pids-limit','--memory','--user','--mount','--cidfile'):
        assert flag in cmd
    assert 'print(42)' not in ' '.join(cmd)


def test_execution_endpoint_validation(client):
    r=client.post('/api/code/execute',json={'language':'python','code':'a'*41000})
    assert r.status_code==422


def test_dev_client_access_unaffected(client,monkeypatch):
    monkeypatch.delenv('STUDIO_WORKER_TOKEN',raising=False)
    assert client.get('/api/health').status_code==200


def test_voice_gate_detects_silence_end():
    from app.audio_live import VoiceGate
    gate=VoiceGate()
    assert gate.push([0.0]*4000) is None
    for _ in range(3): assert gate.push([0.1]*4000) is None
    completed=None
    for _ in range(5):
        result=gate.push([0.0]*4000)
        if result is not None:completed=result;break
    assert completed and len(completed)>=4
    assert gate.frames==[] and not gate.voiced


def test_audio_device_missing_reports_capability(client, monkeypatch):
    from app import audio_live
    monkeypatch.setattr(audio_live.live_audio,'device_list',lambda:{'available':False,'devices':[],'reason':'Not installed'})
    assert client.get('/api/audio/devices').json()['available'] is False
    assert client.get('/api/audio/status').json()['speaker_identification'].startswith('unknown')
    assert client.post('/api/audio/start',json={'source_ids':[]}).status_code==422


def test_audio_event_stream_uses_unknown_speaker(client):
    from app.audio_live import LiveAudio
    from app import audio_live
    old=audio_live.live_audio
    audio_live.live_audio=LiveAudio()
    try:
        audio_live.live_audio.emit('transcript_final',source_id='test-mic',text='Hello',speaker='unknown')
        events=client.get('/api/audio/events?since=0').json()['events']
        assert events[0]['speaker']=='unknown'
        assert client.get('/api/audio/events?since=1').json()['events']==[]
    finally:audio_live.live_audio=old
