"""v0.6 security, consent, AI usage and adapter regression contracts.

Provider calls use HTTP fixtures and are not labelled real Ollama/OpenAI tests.
"""
import asyncio
import json
import os
import sqlite3
import httpx
from app import credentials, db, config, providers
from app.main import ACTIVE_GENERATIONS


def test_cloud_defaults_private(client, monkeypatch):
    monkeypatch.setattr(config, 'ALLOW_CLOUD', False)
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    status=client.get('/api/cloud/status').json()
    assert status['consent'] is False and status['has_key'] is False
    assert status['cloud_requests'].startswith('only explicitly')


def test_consent_roundtrip_persists_only_boolean(client, monkeypatch):
    monkeypatch.setattr(config, 'ALLOW_CLOUD', False)
    r=client.post('/api/cloud/consent',json={'enabled':True})
    assert r.status_code==200 and r.json()['consent'] is True
    assert db.setting('cloud_consent')=='true'
    assert client.post('/api/cloud/consent',json={'enabled':False}).json()['consent'] is False
    assert db.setting('cloud_consent')=='false'


def test_credential_unavailable_fails_closed(client, monkeypatch):
    monkeypatch.setattr(credentials.sys,'platform','linux')
    assert client.post('/api/cloud/credential',json={'api_key':'sk-test-credential-123456789'}).status_code==503
    assert client.delete('/api/cloud/credential').status_code==503


def test_credential_validation_rejects_control_chars():
    for value in ('short', 'x'*1025, 'a'*12+'\nmalicious'):
        try: credentials.save_api_key(value)
        except ValueError: pass
        else: assert False, 'invalid credentials must be rejected before OS interaction'


def test_credential_is_masked_never_in_export(client, monkeypatch):
    saved={}
    monkeypatch.setattr(credentials, 'save_api_key', lambda k:saved.update(key=k))
    monkeypatch.setattr(credentials, 'read_api_key', lambda:saved.get('key'))
    secret='sk-test-secret-not-for-logs-98765'
    r=client.post('/api/cloud/credential',json={'api_key':secret})
    assert r.status_code==200 and secret not in r.text and 'masked' in r.json()
    assert client.get('/api/cloud/status').json()['has_key'] is True
    exported=json.dumps(client.get('/api/export').json())
    assert secret not in exported
    with db.connect() as cx:
        assert secret not in repr(cx.execute('SELECT * FROM settings').fetchall())


def test_inference_metrics_and_delete_cascade(client, monkeypatch):
    class MockProvider:
        async def stream(self,messages,model):
            yield 'An index '
            yield 'makes lookup faster.'
    monkeypatch.setattr(providers,'get_provider',lambda provider:(MockProvider(),'fake-model'))
    sid=client.post('/api/sessions').json()['id']
    stream=client.post('/api/ask/stream',json={'session_id':sid,'question':'Why indexes?'}).text
    assert 'first_token_ms' in stream and 'output_characters' in stream
    entries=client.get('/api/ai/usage').json()['entries']
    assert len(entries)==1 and entries[0]['output_characters']==29
    assert entries[0]['model']=='fake-model' and entries[0]['first_token_ms']>=0
    assert 'token_usage' in client.get('/api/ai/usage').json()
    assert len(client.get(f'/api/sessions/{sid}/ai/usage').json()['entries'])==1
    client.delete(f'/api/sessions/{sid}')
    assert client.get('/api/ai/usage').json()['entries']==[]


def test_usage_unknown_session(client):
    assert client.get('/api/sessions/unknown/ai/usage').status_code==404


def test_explicit_cancel_removes_active_generation(client):
    sid='mock-session-id'
    ACTIVE_GENERATIONS[sid]=object()
    assert client.post(f'/api/ask/{sid}/cancel').json()['cancelled'] is True
    assert sid not in ACTIVE_GENERATIONS
    assert client.post(f'/api/ask/{sid}/cancel').json()['cancelled'] is False


def test_schema_v5_migrates_to_v6_preserving_transcripts(client):
    sid=client.post('/api/sessions').json()['id']
    client.post(f'/api/sessions/{sid}/transcripts',json={'text':'test sentence','source_id':'microphone'})
    with db.connect() as cx:
        cx.execute('DROP TABLE ai_usage')
        cx.execute('PRAGMA user_version=5')
    db.initialize()
    assert client.get(f'/api/sessions/{sid}/transcripts').json()['transcripts'][0]['text']=='test sentence'
    with db.connect() as cx:
        assert cx.execute('PRAGMA user_version').fetchone()[0]==7
        assert cx.execute('PRAGMA foreign_key_check').fetchall()==[]


def test_ollama_fake_http_stream_safe_errors(client, monkeypatch):
    real=httpx.AsyncClient
    def handler(request):
        if request.url.path.endswith('/api/chat'):
            return httpx.Response(404, text='a sensitive prompt should not echo in UI')
        return httpx.Response(500)
    monkeypatch.setattr(providers.httpx,'AsyncClient',lambda *a,**kw:real(transport=httpx.MockTransport(handler),**kw))
    async def check():
        try:
            async for _ in providers.Ollama('ollama').stream([{'role':'user','content':'private'}],'missing'):pass
        except providers.ProviderError as e:
            assert 'HTTP 404' in str(e)
            assert 'sensitive' not in str(e)
        else: assert False
    asyncio.run(check())


def test_cloud_retry_429_before_tokens_then_stream(client, monkeypatch):
    real=httpx.AsyncClient
    attempts=[]
    def handler(request):
        attempts.append(request)
        assert request.headers['Authorization']=='Bearer dummy-key'
        if len(attempts)==1:return httpx.Response(429)
        return httpx.Response(200,text='data: {"choices":[{"delta":{"content":"Good"}}]}\n\ndata: [DONE]\n\n',headers={'Content-Type':'text/event-stream'})
    monkeypatch.setattr(providers.httpx,'AsyncClient',lambda *a,**kw:real(transport=httpx.MockTransport(handler),**kw))
    monkeypatch.setattr(credentials,'read_api_key',lambda:'dummy-key')
    db.set_setting('cloud_consent','true')
    async def check():
        chunks=[]
        async for token in providers.OpenAICompatible('cloud').stream([{'role':'user','content':'prompt'}],'test-model'):
            chunks.append(token)
        return chunks
    assert asyncio.run(check())==['Good']
    assert len(attempts)==2


def test_cloud_401_error_hides_response(client, monkeypatch):
    real=httpx.AsyncClient
    def handler(request):return httpx.Response(401,text='secret details in error')
    monkeypatch.setattr(providers.httpx,'AsyncClient',lambda *a,**kw:real(transport=httpx.MockTransport(handler),**kw))
    monkeypatch.setattr(credentials,'read_api_key',lambda:'dummy-key')
    db.set_setting('cloud_consent','true')
    async def check():
        try:
            async for _ in providers.OpenAICompatible('cloud').stream([],'test'):pass
        except providers.ProviderError as e:
            assert '401' in str(e) and 'secret details' not in str(e)
        else:assert False
    asyncio.run(check())


def test_cloud_never_auto_fallback(client, monkeypatch):
    monkeypatch.setattr(config,'ALLOW_CLOUD',False)
    db.set_setting('cloud_consent','false')
    monkeypatch.setattr(credentials,'read_api_key',lambda:'dummy-key')
    async def check():
        try:
            async for _ in providers.OpenAICompatible('cloud').stream([],'model'):pass
        except providers.ProviderError as e:assert 'Cloud disabled' in str(e)
        else:assert False
    asyncio.run(check())


def test_disabling_cloud_overrides_legacy_env_opt_in(client, monkeypatch):
    monkeypatch.setattr(config, 'ALLOW_CLOUD', True)
    assert client.get('/api/cloud/status').json()['consent'] is True
    client.post('/api/cloud/consent',json={'enabled':False})
    assert client.get('/api/cloud/status').json()['consent'] is False
    assert providers.OpenAICompatible._consent() is False
