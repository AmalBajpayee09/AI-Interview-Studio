"""v0.7 regression: redacted credential errors and real Windows vault round-trip.

The local provider-frame test uses deterministic HTTP responses, NOT a real AI model.
"""
import asyncio
import sys
import uuid
import pytest
import httpx
from app import credentials, providers


def test_bad_cloud_key_not_reflected_in_pydantic_error(client):
    secret='sk-test-should-not-echo-12345'
    invalid=client.post('/api/cloud/credential',json={'api_key':'short'})
    assert invalid.status_code == 400
    assert 'short' not in invalid.text
    malformed=client.post('/api/cloud/credential',content='{"api_key": "'+secret+'"',
                          headers={'content-type':'application/json'})
    assert malformed.status_code == 400
    assert secret not in malformed.text


def test_real_wincred_round_trip():
    if sys.platform != 'win32':
        pytest.skip('Requires native Windows Credential Manager.')
    old=credentials.TARGET
    credentials.TARGET='AIInterviewStudio/TemporaryTest-'+uuid.uuid4().hex
    value='sk-wincred-real-test-123456'
    try:
        assert credentials.read_api_key() is None
        credentials.save_api_key(value)
        assert credentials.read_api_key()==value
        assert credentials.delete_api_key() is True
        assert credentials.read_api_key() is None
    finally:
        try: credentials.delete_api_key()
        finally: credentials.TARGET=old


def test_malformed_ollama_json_sanitized(monkeypatch):
    async def check():
        original=httpx.AsyncClient
        transport=httpx.MockTransport(lambda request: httpx.Response(200,text='[1,2,3]\\n'))
        monkeypatch.setattr(httpx,'AsyncClient',lambda *a,**k: original(transport=transport))
        try:
            await anext(providers.Ollama('ollama').stream([{'role':'user','content':'hello'}],'test'))
            assert False, 'expected failure'
        except providers.ProviderError as err:
            assert 'invalid streaming data' in str(err)
    asyncio.run(check())
