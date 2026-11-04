"""Opt-in genuine Ollama cancellation and session continuation over a running worker.

No MockTransport, fake model or simulated streaming. Requires an Ollama
service with an already installed model. This is not Windows desktop acceptance.
"""
import json
import os
import secrets
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("STUDIO_LIVE_OLLAMA_TEST") != "1",
    reason="requires real Ollama server and installed local model",
)


def _frames(response):
    for line in response.iter_lines():
        if line.startswith("data: "):
            yield json.loads(line[6:])


def test_real_ollama_cancellation_and_authenticated_retry(tmp_path):
    service = Path(__file__).resolve().parents[1]
    model = os.getenv("STUDIO_TEST_OLLAMA_MODEL", "smollm2:135m")
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    secret = secrets.token_urlsafe(40)
    env = {**os.environ,
        "STUDIO_PORT": str(port),
        "STUDIO_WORKER_TOKEN": secret,
        "STUDIO_DATA_DIR": str(tmp_path / "state"),
        "STUDIO_DIAGNOSTIC_DIR": str(tmp_path / "logs"),
        "PYTHONPATH": str(service),
        "OLLAMA_URL": os.getenv("OLLAMA_URL", "http://127.0.0.1:11434"),
    }
    base = f"http://127.0.0.1:{port}"
    headers = {"X-Studio-Token": secret}
    proc = subprocess.Popen(
        [sys.executable, str(service / "run_worker.py")],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        with httpx.Client(timeout=httpx.Timeout(120, connect=4)) as client:
            deadline = time.monotonic() + 25
            while time.monotonic() < deadline:
                if proc.poll() is not None:
                    raise AssertionError("Worker exited before authenticated readiness")
                try:
                    r = client.get(base + "/api/health", headers=headers)
                    if r.status_code == 200 and r.json()["version"] == "1.0.0-rc.3":
                        break
                except httpx.RequestError:
                    pass
                time.sleep(0.1)
            else:
                raise AssertionError("Live worker never authenticated")
            assert client.get(base + "/api/health").status_code == 401
            sid = client.post(base + "/api/sessions", headers=headers,
                              json={"title": "Synthetic genuine Ollama cancellation"}).json()["id"]
            assert sid
            cancellation = None
            got_first_token = False
            got_error = False
            with client.stream(
                "POST", base + "/api/ask/stream",
                json={"session_id": sid, "provider": "ollama", "model": model,
                      "question": "Write a long list of 100 practical programming lessons, numbering each item and explaining it."},
                headers=headers,
            ) as reply:
                assert reply.status_code == 200, reply.text
                for event in _frames(reply):
                    if event["type"] == "token" and not got_first_token:
                        got_first_token = True
                        cancel = client.post(base + f"/api/ask/{sid}/cancel", headers=headers)
                        assert cancel.status_code == 200, cancel.text
                        cancellation = cancel.json()
                        assert cancellation["cancelled"], cancellation
                    elif event["type"] == "error":
                        assert "cancel" in event["message"].lower(), event
                        got_error = True
                        break
                    elif event["type"] == "done":
                        raise AssertionError("Live model completed before cancellation was honored")
            assert got_first_token and cancellation and got_error
            assert client.get(base + f"/api/sessions/{sid}/turns",headers=headers).json() == []
            # A completed request after cancellation must still be accepted.
            with client.stream(
                "POST", base + "/api/ask/stream",
                json={"session_id": sid, "provider": "ollama", "model": model,
                      "question": "What is a stack data structure? Answer briefly."},
                headers=headers,
            ) as reply:
                assert reply.status_code == 200
                sequence = list(_frames(reply))
            assert sequence and sequence[-1]["type"] == "done", sequence[-1]
            assert any(e["type"] == "token" for e in sequence)
            assert sequence[-1]["first_token_ms"] is not None
            turns = client.get(base + f"/api/sessions/{sid}/turns", headers=headers).json()
            assert len(turns) == 1 and turns[0]["provider"] == "ollama"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill(); proc.wait(timeout=8)
    logs = (tmp_path / "logs" / "worker-startup.jsonl").read_text(encoding="utf-8")
    assert secret not in logs
