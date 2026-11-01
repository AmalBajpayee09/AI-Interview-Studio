# AI Interview Studio — source preview 0.4.0

> **v0.3 status:** Tested Python source preview, not a Windows release. There is no installer until a Windows build completes. Full React compilation, native Rust integration and genuine model/audio/device tests are still pending. Read [v0.3 release gate](docs/RELEASE_GATE_V03.md) before evaluating the product.

## v0.3 additions (incremental)

- Bundled worker design now uses a randomized loopback port and per-launch secret managed by Tauri; requests from the React app use authenticated headers. Standalone development browser mode remains local-only and unauthenticated.
- Optional Docker-isolated code runner for Python, JavaScript, C++, Java, with manual image setup, stdin/expected output, resource limits and safe disabled state without Docker.
- Experimental opt-in multiple-source capture (mic + supported loopback input), bounded audio segmentation, and local Whisper final transcription events. Source is not speaker identity, so true diarization remains unimplemented.
- Windows CI has real compile, tests, PyInstaller, NSIS and artifact steps. The uploaded v0.2 source omitted a dependency lock; the first CI job resolves one and must have its resulting lockfile committed for reproducible releases.
- Added regression tests and localhost authentication smoke measurements.

Documentation: [v0.3 audit](docs/IMPLEMENTATION_AUDIT_V03.md), [Windows release](docs/WINDOWS_RELEASE_V03.md), [code execution](docs/CODE_EXECUTION_V03.md), [live audio](docs/AUDIO_LIVE_V03.md), [security](docs/SECURITY_V03.md), [release gate](docs/RELEASE_GATE_V03.md).


An **actual runnable local interview-practice backend and browser companion**, plus source code for a Tauri 2 / Rust / React / TypeScript Windows desktop shell. Designed for authorized self-study and mock interviews. This is a **preview**, not a fully tested Windows release. The original 58-page specification and the 22-page completion add-on are retained at `docs/USER_REQUIREMENTS.pdf` and `docs/COMPLETION_ADDON.pdf` so the requirements remain available with the project.

## What works

- FastAPI localhost service with SQLite migrations, transactions, 30-day configurable retention, session history, deletion, and export.
- Context-aware, cancellable streamed AI practice answers through local **Ollama** and explicit-opt-in **OpenAI** HTTP adapters; requests use recent turns plus selected snippets from user-provided documents.
- Session-linked follow-ups, seven answer modes and question classification, all with honest verification labels.
- Multiple-choice practice assessments: sample bank, validated custom question JSON, countdown, persisted/resumable answer drafts, review marks, negative marking, explanations and analytics. Partial-credit scoring is not yet implemented.
- SQL laboratory with a read-only three-table training dataset, restricted query authorizer, timeouts and verifiable result tables.
- SQLite-consistent backup download and offline restore utility.
- Persisted advisory resource profiles for battery saver, balanced and performance.
- Python-only static code syntax checking (never executes generated code), coding-review prompts, system design and ML practice prompts.
- User-uploaded PDF, DOCX, text and image OCR where dependencies permit. OCR is fallible; extracted content is editable before saving. Files have size limits.
- Text-based communication pace/filler feedback; microphone recording and transcription endpoint available *optionally* through `faster-whisper`, loaded only on demand. The default package contains no downloaded AI weights.
- React UI for Windows-native Tauri (requires unverified native build), and a dependency-free browser companion served by Python at `/`.
- Visible compact always-on-top Tauri window command. No anti-proctoring bypass or unauthorized capture controls.

## Quick start without Node/Rust (the tested fallback)

From PowerShell in the extracted project root (requires Python 3.11):

```powershell
py -3.11 -m venv services\ai_worker\.venv
.\services\ai_worker\.venv\Scripts\python.exe -m pip install -r services\ai_worker\requirements.txt
Copy-Item .env.example .env
.\scripts\run-browser.ps1
```

A browser opens at http://127.0.0.1:8765. Offline assessments, session history, extraction, diagnostics and syntax checks work without AI keys or model downloads. Answer generation needs Ollama with a downloaded model or explicitly configured cloud inference.

## Windows native desktop setup

See [the beginner Windows guide](docs/WINDOWS_SETUP.md) and PowerShell scripts. Native build requires **Node LTS, Rust stable MSVC, Visual Studio C++ Build Tools, and WebView2**. Official prerequisites: https://v2.tauri.app/start/prerequisites/. Run `./scripts/setup.ps1` then `./scripts/dev.ps1` for development. `./scripts/build.ps1` attempts to bundle the Python worker via PyInstaller and build an NSIS installer on Windows. **This has NOT been tested on Windows in this build environment**. The React frontend could not be compiled here because npm registry access was unavailable; Rust/Cargo were also unavailable.

## Architecture

`apps/desktop/src` React UI → browser/WebView loopback HTTP API → FastAPI/Pydantic worker → SQLite / OCR / STT / Ollama / explicit opt-in cloud. A narrowly scoped Rust command handles compact window sizing and topmost state; Windows release packaging may embed a PyInstaller worker. The app is intentionally **not** a privileged Windows service. See [ARCHITECTURE](docs/ARCHITECTURE.md), [HLD](docs/HLD.md), [LLD](docs/LLD.md), and [SECURITY](docs/SECURITY.md).

## Upgrade and testing status

See `docs/IMPLEMENTATION_AUDIT.md`, `docs/ADDON_COMPLETION_STATUS.md`, `docs/TEST_REPORT.json` and `docs/BENCHMARK_V02.json` for exactly what was implemented, measured and blocked. **32 automated Python tests and five real localhost HTTP smoke checks passed**. Frontend production build and Rust compilation are still blocked by missing dependencies/tooling. No Windows installer has been generated. A Windows CI workflow is provided but has not run here.

## Status and limits

- **Implemented + tested here:** API and database, MCQ scoring, sessions, document CRUD, diagnostics, static code syntax, logic and communication feedback, HTTP interface and explicit cloud opt-in checks. Tests and measured results are in `docs/RELEASE_CHECKLIST.md` and `docs/BENCHMARK.json`.
- **Implemented but not validated in this environment:** React build, Rust/Tauri build, packaged worker, Windows installer, local Ollama and cloud provider live streaming, OCR on Windows, real speech transcription, Windows on-top window.
- **Partial / not implemented:** continuous low-latency dual-channel system audio, speaker diarization, microphone device selection, robust Hindi/Hinglish STT benchmarks, streaming multimodal image reasoning, automated hidden-test verification, genuine sandboxed execution of untrusted code, partial credit and additional assessment types, virtual audio, GPU resource governor, multi-monitor testing, accessibility audit, signed auto-updates and mature ML analytics.
- **Not implemented:** modifications to Safe Exam Browser that disable kiosk security, monitoring or proctoring; screen-share invisibility; process stealth; bypass of secure assessment restrictions. Mock testing can use ordinary authorized windows and logged capture observations. See `docs/SEB_MOCK_TESTING.md`.

No application can promise OCR is always correct, hidden coding tests always pass, or full useful answers always arrive within 1–2 seconds. Actual performance depends on local models and hardware.

## Project structure

```text
apps/desktop/             React frontend and Tauri/Rust desktop shell
services/ai_worker/       Python API, provider adapters, SQLite, tests, static companion
scripts/                  PowerShell setup, run, tests, diagnostic and build tasks
docs/                     Original specification, setup, architecture, risks and results
shared/                   Typed data contract reference
```

## Security and privacy

- Bind the API only to `127.0.0.1:8765`. Origin and Host validation is included. **Loopback has no authentication** and should not be exposed to public networks or used on an untrusted shared machine without additional protection.
- Cloud is off until `ALLOW_CLOUD=true` and `OPENAI_API_KEY` exist; user is responsible for permission to send submitted content. Keys are kept out of SQLite but may be stored in a plaintext local `.env` file; restrict filesystem access accordingly (OS vault integration is pending).
- The worker uses 30-day retention on startup, no raw audio storage; temporary audio files are deleted. Document content is stored in SQLite without encryption at rest. Avoid uploading secrets unless you trust your machine.
- Do not run arbitrary AI-generated code in the desktop app. Syntax check is not code execution.

## License

Source created for this project: MIT (see `LICENSE`). Original Safe Exam Browser archive is a separate third-party MPL-2.0 project and **is not repackaged or modified here**.

For a requirement-by-requirement overview see `docs/REQUIREMENTS_MATRIX.md`. For errors see `docs/TROUBLESHOOTING.md`.

## New in v0.2.0

Use **SQL lab** to run read-only queries against the included dataset, resume partially completed quizzes across worker restarts, download your SQLite backup from Settings, or run `scripts/restore-database.py` after stopping the worker. See [User guide](docs/USER_GUIDE.md), [SQL practice](docs/SQL_PRACTICE.md), [Audio](docs/AUDIO_SETUP.md), [Developer guide](docs/DEVELOPER_GUIDE.md) and [Dependency summary](docs/DEPENDENCIES_LICENSES.md).
