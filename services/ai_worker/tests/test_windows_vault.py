"""Runs only in opt-in ephemeral Windows CI OS account.

Never touch the user's real saved OpenAI key; substitute unique target ID.
"""
import os
import sys
import uuid
import pytest
from app import credentials

@pytest.mark.skipif(sys.platform!='win32' or os.getenv('STUDIO_WINDOWS_VAULT_TEST')!='1',
                    reason='Requires opt-in ephemeral Windows runner Credential Manager')
def test_real_windows_credential_manager_read_write_delete(monkeypatch):
    target='AIInterviewStudio/CI/'+str(uuid.uuid4())
    monkeypatch.setattr(credentials,'TARGET',target)
    secret='sk-ci-ephemeral-'+str(uuid.uuid4())
    try:
        assert credentials._read_windows_key() is None
        credentials.save_api_key(secret)
        assert credentials._read_windows_key()==secret
        assert credentials.has_api_key() is True
        assert credentials.delete_api_key() is True
        assert credentials._read_windows_key() is None
    finally:
        credentials.delete_api_key()
