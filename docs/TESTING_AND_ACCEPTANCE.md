# Testing and acceptance — v0.5.0

## Executed here (Linux host, not Windows)

- Baseline: **51/51 Python tests passed** before modifications.
- v0.5: **60/60 Python tests passed** (`PYTHONPATH=services/ai_worker python -m pytest services/ai_worker/tests -q`). Test log: `docs/V05_PYTEST.xml`.
- TypeScript/TSX **syntax transpilation**: 9/9 source files, 0 parse diagnostics using globally available TypeScript (this does **not** check types, execute React, or build Vite assets).
- `npm ci --offline` failed (`ENOTCACHED` on Vite archive); `npm run build` was therefore not executed here.
- Rust/Cargo compilation: **not run**, toolchain unavailable on this Linux host.
- Docker execution: **not run**, Docker CLI/engine unavailable (tests use mocked subprocess interfaces).
- Microphone/Windows loopback and genuine STT: **not run**, missing Windows devices/model runtime.
- Genuine Ollama/cloud AI: **not run** with a configured model/credential. Mock provider test is **not** real inference.

## Evidence categories

- `test_v05.py` checks three MCQ modes, numerical tolerance, missing/negative scoring, validation, persisted drafts, opt-in transcript creation/export/recovery/deletion, session isolation, cascade deletion, schema v4→v5 migration and backup restore integrity.
- `test_v04.py` checks audio pause/resume state and bounded events; Docker command restrictions/out-limit using fake subprocesses.
- `test_upgrade.py` checks SQL read-only enforcement, timeout, custom assessment validation, SQLite migration, backup, resource mode.
- `test_studio.py` checks sessions, mock streamed answer persistence, parsing, file extraction, basic communication feedback, export and origin restriction.

## Eight acceptance journeys (v0.5.0)

| Journey | Verified subset | Still required |
|---|---|---|
| Interview | Mock provider streamed answer + SQLite turn persistence | Live Ollama/cloud, Windows UI, continuous questions, follow-ups |
| Coding | Docker refusal + test-suite contract unit tests | Actual isolated container execution and Windows UI |
| Assessment | API single/multiple/numerical scoring, drafts, restore | Compiled frontend, timer/restart and full report QA |
| Audio | Voice gate unit + event mocks, opt-in transcript persistence | Real devices, latency, diarization, recovery |
| Resume | Text ingestion basic checks, retrieval logic exists | Real resume evidence retrieval and user correction flow |
| ML | Routed prompts to interview workspace | Dedicated mathematical/ML system design workflows and evaluation |
| Recovery | SQLite idempotent migration, drafts, transcripts, backup | Installed Windows crash/restart/upgrade |
| Release | Historical v0.4 Windows smoke and packaging success | v0.5 Windows build, install, UI workflows, upgrade, uninstall |

## Windows follow-up commands

```powershell
cd apps/desktop
npm ci
npm run build
cd src-tauri
cargo check
cargo test
cd ..\..\..
$env:PYTHONPATH = 'services/ai_worker'
py -3.11 -m pytest services/ai_worker/tests -q
.\scripts\build.ps1
```

Record real runner job URLs and SHA-256 output; do not confuse Vite compilation with interactive UI acceptance.
