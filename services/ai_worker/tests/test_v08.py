"""v0.8 integration contracts. Simulated provider is NOT live AI evidence."""
import asyncio
import json
import os
import time
import pytest
import httpx
from app import providers, db, config
from app.main import ACTIVE_GENERATIONS


def _frames(response):
    return [json.loads(line[6:]) for line in response.text.splitlines() if line.startswith('data: ')]


def test_completed_stream_includes_measured_first_token_latency(client, monkeypatch):
    class Stub:
        async def stream(self, messages, model):
            yield 'Measured '
            yield 'output'
    monkeypatch.setattr(providers, 'get_provider', lambda _: (Stub(), 'mock'))
    sid = client.post('/api/sessions').json()['id']
    response = client.post('/api/ask/stream', json={'session_id':sid,'question':'Question?'})
    assert response.status_code == 200
    frames = _frames(response)
    assert [f['type'] for f in frames] == ['meta','token','token','done']
    done = frames[-1]
    assert isinstance(done['first_token_ms'], int) and done['first_token_ms'] >= 0
    assert done['first_token_ms'] <= done['elapsed_ms']
    assert done.get('output_characters',done.get('characters')) == len('Measured output')
    assert len(client.get(f'/api/sessions/{sid}/turns').json()) == 1


def test_stream_rejects_concurrent_session_generation_without_mutating_active(client,monkeypatch):
    sid=client.post('/api/sessions').json()['id']
    active=object(); ACTIVE_GENERATIONS[sid]=active
    try:
        response=client.post('/api/ask/stream',json={'session_id':sid,'question':'Duplicate question'})
        assert response.status_code==409
        assert ACTIVE_GENERATIONS[sid] is active
        assert client.get(f'/api/sessions/{sid}/turns').json()==[]
    finally:
        ACTIVE_GENERATIONS.pop(sid,None)


def test_stream_cancel_does_not_save_partial_text(client,monkeypatch):
    sid=client.post('/api/sessions').json()['id']
    class Stub:
        async def stream(self, messages, model):
            yield 'one'
            ACTIVE_GENERATIONS.pop(sid,None)
            yield 'two'
    monkeypatch.setattr(providers,'get_provider',lambda _: (Stub(),'mock'))
    frames=_frames(client.post('/api/ask/stream',json={'session_id':sid,'question':'Cancel'}))
    assert frames[-1]['type']=='error'
    assert 'cancel' in frames[-1]['message'].lower()
    assert client.get(f'/api/sessions/{sid}/turns').json()==[]


def test_local_provider_error_cannot_echo_ollama_generated_secrets(monkeypatch):
    async def check():
        reply={'error':'Sensitive session transcript sk-PRIVATE-1234'}
        transport=httpx.MockTransport(lambda _:httpx.Response(200,text=json.dumps(reply)+'\n'))
        original=httpx.AsyncClient
        monkeypatch.setattr(httpx,'AsyncClient',lambda *a,**kw: original(transport=transport))
        with pytest.raises(providers.ProviderError) as e:
            await anext(providers.Ollama('ollama').stream([{'role':'user','content':'hi'}],'foo'))
        assert 'sk-PRIVATE' not in str(e.value)
    asyncio.run(check())


def test_session_persists_answer_through_sqlite_reinitialize(client,monkeypatch):
    class Stub:
        async def stream(self,messages,model): yield 'Answer persists.'
    monkeypatch.setattr(providers,'get_provider',lambda _: (Stub(),'mock'))
    sid=client.post('/api/sessions',json={'title':'recovery'}) .json()['id']
    assert _frames(client.post('/api/ask/stream',json={'session_id':sid,'question':'What is persistence?'}))[-1]['type']=='done'
    db.initialize()
    saved=client.get(f'/api/sessions/{sid}/turns').json()
    assert len(saved)==1 and saved[0]['answer']=='Answer persists.'


@pytest.mark.skipif(os.getenv('STUDIO_LIVE_OLLAMA_TEST')!='1',reason='Real Ollama test requires STUDIO_LIVE_OLLAMA_TEST=1 and an installed model')
def test_real_ollama_generation_opt_in():
    """Only passing test here may count as actual model execution; never a MockTransport."""
    async def run():
        models=await providers.list_local_models()
        assert models['online'] and models['models'], 'Start Ollama and install a model first'
        name=models['models'][0]
        tokens=[]
        async for token in providers.Ollama('ollama').stream([{'role':'user','content':'In a single short sentence, define a stack data structure.'}],name):
            tokens.append(token)
            if len(''.join(tokens))>=120: break
        assert ''.join(tokens).strip()
    asyncio.run(run())


@pytest.mark.skipif(os.getenv('STUDIO_LIVE_CLOUD_TEST')!='1',reason='Live cloud test requires STUDIO_LIVE_CLOUD_TEST=1, explicit consent and credentials')
def test_real_cloud_generation_opt_in():
    """Never automatically sends data off-device in CI."""
    assert providers.OpenAICompatible._consent() and providers.credentials.read_api_key(), 'Explicit cloud consent and credential required'
    async def run():
        stream=providers.OpenAICompatible('cloud').stream([{'role':'user','content':'Say OK only.'}],config.CLOUD_MODEL)
        tokens=[]
        async for token in stream:
            tokens.append(token)
            if len(''.join(tokens))>=12: break
        assert ''.join(tokens).strip()
    asyncio.run(run())
