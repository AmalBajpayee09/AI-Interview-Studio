# v0.4.0 release gate — evidence-based engineering report

## Environment
This source package was inspected and tested in a Debian 13 Linux container, Python 3.13.5, Node.js 22.16.0, globally installed TypeScript 5.8.3. It does not have Rust/Cargo, Docker Engine, Windows 10/11, a Windows microphone, the optional SoundCard/faster-whisper packages, or online npm registry access. GitHub can be accessed through the connected GitHub integration but that integration cannot directly import the user's binary ZIP as an unpacked repository tree.

## Evidence
- Python regression suite: **51 passed** via `PYTHONPATH=services/ai_worker pytest -q services/ai_worker/tests`.
- Actual locally launched HTTP worker: measured health endpoint and SQL/session routes; see `docs/V04_BENCHMARK.json`. The worker was launched as a separate subprocess using local ephemeral data and terminated after checks.
- TypeScript syntactic transpilation: **9 files parsed with zero diagnostics**. This is NOT a React production build or complete type check.
- `npm ci --offline`: **failed** because `apps/desktop/package-lock.json` was absent. `npm view` failed with EAI_AGAIN because the npm registry could not be resolved. Do not create a fake lockfile.
- `cargo` and `rustc`: unavailable. The native Windows application was NOT built.
- `docker`: unavailable. Container execution refused by design; unit tests use mocks. No actual code execution passed under Docker.
- Windows installer, signed MSI, portable executable, install/restart/upgrade/uninstall: **BLOCKED, NOT PRODUCED**.
- Genuine Ollama/cloud provider tests: **NOT EXECUTED**, no configured runtime/credentials.
- Live audio devices, source separation, speaker diarization, and real speech latency: **NOT EXECUTED**. Source attribution is NOT speaker diarization.

## v0.4 improvements actually implemented
| Area | Status | Evidence |
| --- | --- | --- |
| Existing SQLite/session/assessment functionality | PASS (backend tests) | 41 previously passing tests retained |
| Audio pause/resume and event timestamps | PARTIAL | New mocked lifecycle tests; real microphone unavailable |
| Multiple coding test cases | PARTIAL | Endpoint and mock tests; Docker runtime absent |
| Code execution output-size kill switch | PARTIAL | Mock output-flood test; real container untested |
| Local saved coding drafts by language | PASS (backend tests) | Read/write/delete tests and UI controls |
| React UI coding and audio controls | PARTIAL | TSX transpilation only; no browser E2E |
| Desktop Python worker packaging | BLOCKED | PyInstaller and Windows host unavailable |
| React production build | BLOCKED | Missing lockfile and npm registry access |
| Rust/Tauri native compilation | BLOCKED | Rust/Cargo absent |
| Windows installer and portable release | BLOCKED | No native Windows build or CI run |
| Full GitHub source import | BLOCKED | Uploaded ZIP cannot be transmitted by the available GitHub connector as a source tree; bundled import helper included |

The application is an **engineering source preview**, not a finished installable Windows product. Do not label it fully production-ready.

## Executed GitHub Windows CI evidence
The [real Windows CI run #41346727566](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41346727566) **FAILED** on November 1, 2026 UTC. The checkout, Python setup, Node setup and Rust toolchain steps all completed. The `Verify complete source import` step failed: `Missing source or lockfile: apps/desktop/package.json. Import full v0.4.0 project before compiling.` All React, Rust compile, worker packaging and installer-generation stages were skipped. No installer artifact was produced.

The source archive includes `scripts/publish-github.ps1`, but it has **not been executed** in this environment because outbound git network connections and npm registry resolution are blocked here. The full source has not yet been published to the GitHub repo. The Windows workflow and import instructions are committed there.
