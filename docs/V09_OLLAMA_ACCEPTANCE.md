# v0.9 real local Ollama acceptance

**Local environment:** `ollama` executable absent; request to `http://127.0.0.1:11434/api/tags` returned connection-refused. No model files or local GPU/accelerator were available. **Real Ollama inference was NOT run** and cannot be claimed passed.

The application retains the original Ollama `/api/tags` catalogue and `/api/chat` streaming adapter, including sanitized provider errors and no silent cloud fallback. The v0.9 Tauri readiness handshake authenticates the packaged worker, **not** Ollama; they are separate checks.

## Exact opt-in real-provider procedure on Windows

1. Install Ollama from its official Windows instructions, run it and pull a model compatible with your machine. Do not claim a model's performance without measuring it.
2. In PowerShell run `Invoke-RestMethod http://127.0.0.1:11434/api/tags` and verify the chosen model name is listed.
3. Open AI Interview Studio. In **Live practice**, choose `Local · Ollama`, enter a model name from the discovered catalogue, start a new practice session, then submit: “Explain a stack in one sentence.” Confirm streamed tokens render and the response is saved in that session.
4. Submit a follow-up in the *same* session. Inspect stored turns and confirm the follow-up actually uses the prior exchange.
5. During a new long generation, select **Cancel**. Verify the partial answer is not saved. Retry and ensure only the completed answer is stored.
6. Stop Ollama during a generation; verify the UI reports the provider failure, and then restart Ollama and retry.
7. Close and reopen the desktop application; recover the session from the history menu, checking turn order and titles.
8. Record Ollama version, model/digest, Windows version, CPU/GPU/RAM, elapsed timings and actual output; avoid including personal prompts in shared diagnostics.

The optional executable integration test is:

```powershell
$env:STUDIO_LIVE_OLLAMA_TEST='1'
$env:STUDIO_TEST_OLLAMA_MODEL='your-installed-model-name'
$env:PYTHONPATH='services/ai_worker'
& services/ai_worker/.venv/Scripts/python.exe -m pytest services/ai_worker/tests/test_v09.py -k real_ollama -v
```

This test contacts an **actual live Ollama**, uses the HTTP API to stream two successive answers and verifies SQLite recovery. It uses no MockTransport. The complete installed desktop path must still be manually tested or separately automated; a backend HTTP integration test alone does not satisfy the milestone's end-to-end definition.
