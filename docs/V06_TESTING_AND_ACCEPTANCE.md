# v0.6 testing and acceptance

## Actually run on this Linux host

- `PYTHONPATH=services/ai_worker python -m pytest services/ai_worker/tests -q`: **74 passed, 1 skipped** (skipped real Windows credential vault test).
- `python -m compileall -q services/ai_worker/app`: passed.
- 9 `.ts`/`.tsx` frontend files passed `typescript.transpileModule` syntax diagnostics; **not** a type-check or production bundle.
- `python scripts/v06-http-smoke.py`: **14/14** checks against a live Uvicorn server on localhost, worker-token rejection, origin protection, SQL restrictions, privacy toggles, session/usage endpoints and cancel API.
- `test_v06.py` provider tests use synthetic HTTP responses and fake credentials. They prove adapter logic only, not real provider connectivity.

## Windows CI requirements

Run `.github/workflows/windows-v06-validation.yml` on a real Windows runner. It checks Python 3.11 with `STUDIO_WINDOWS_VAULT_TEST=1` (real Windows CredWrite/Read/Delete using an ephemeral unique vault target), `npm ci`, React production build, `cargo check/test`, PyInstaller and Tauri NSIS package generation.

**Not validated by this workflow alone:** install, upgrade, uninstall, portable execution, target laptop benchmarks, real cloud/Ollama models, actual Docker execution, real microphone/loopback, multi-speaker attribution. These require additional independent acceptance tests.

## Eight critical journeys

Interview: **partial** (session/text + mocked stream; live models untested).
Coding: **partial** (Docker refusal and command tests; actual container untested).
Assessment: **partial** (mixed scoring + drafts through API; Windows UI untested for v0.6).
Audio: **blocked** (Linux test environment lacks Windows devices and real diarization).
Resume: **partial** (document extraction, lexical retrieval; project knowledge graph lacking).
ML: **partial** (prompt-based workflow; no specialized math evaluation).
Recovery: **partial** (SQLite migrations, draft recovery and backups tested; crash and upgrade not).
Release: **blocked pending Windows CI** for v0.6; previous v0.5 installation smoke is historical.
