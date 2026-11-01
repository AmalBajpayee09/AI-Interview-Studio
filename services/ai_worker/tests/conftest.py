import os
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app import config,db
from app.main import app

@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setattr(config,'DATA_DIR',tmp_path)
    monkeypatch.setattr(config,'DB_PATH',tmp_path/'db.sqlite3')
    with TestClient(app) as cli: yield cli
