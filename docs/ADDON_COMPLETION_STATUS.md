# Production completion add-on: evidence-backed v0.2.0 status

Scope: `addon.pdf` (22 pages), continuing the user-uploaded v0.1.0 project. "PASS" means an actual test completed here; "PARTIAL" means code exists but full end-to-end validation is missing; "BLOCKED" means build or validation requires unavailable tools/hardware/providers.

| Requested deliverable | Status | Evidence / limitations |
| --- | --- | --- |
| Preserve existing source and assess gaps | PASS | `IMPLEMENTATION_AUDIT.md`; no baseline feature intentionally removed |
| Python worker endpoints and local session SQLite | PASS | Python test suite, actual HTTP smoke test |
| SQL practice database and safe read-only query editor | PASS | SQLite in-memory dataset; query authorizer, time and output limits; tests for joins, mutation rejection and timeout; React and browser companion SQL views have syntax checks |
| Timed assessment draft recovery | PASS | Version 3 migration, API, UI autosave and recovery, tests; timer uses client time and is **not proctored** |
| Data snapshot backup and offline restoration | PASS | SQLite online backup API, integrity checked restore CLI, end-to-end local tests |
| Advisory resource modes (battery saver, balanced, performance) | PASS | Measured psutil snapshot + persisted mode, test; **not** an active GPU/LLM scheduler |
| Ollama/cloud adapters | PARTIAL | Existing HTTP adapters; real provider calls not possible without local Ollama or credentials |
| Audio speech transcription | PARTIAL | Existing optional file/mic-upload path now emits timestamps with unknown speaker; STT model and live devices unavailable; continuous dual-source diarization not completed |
| Secure isolated code running / hidden tests | BLOCKED | Only Python AST syntax check. A non-isolated subprocess is intentionally not exposed as secure execution; no Docker/Windows isolation runner here |
| Windows Tauri desktop shell | BLOCKED | Source and scripts retained; Rust/Cargo and Windows build environment not installed |
| Actual Windows installer and portable EXE | BLOCKED | Cannot create or validate Windows artifacts on this Linux host. Windows GitHub Actions build workflow and local PowerShell recipe supplied, **unverified** |
| React production build / static typing | BLOCKED | npm registry DNS inaccessible; `tsc` source transpile checks pass for 8 files (not equivalent to production build) |
| Browser companion | PARTIAL | Real HTTP GET and Node JS syntax check pass; live Chromium navigation blocked by container policy |
| Screen overlay | PARTIAL | Existing Tauri compact/always-on-top source; Windows behavior not tested; no monitoring/proctoring bypass |
| AI quality, hardware-specific 1–2 second latency | BLOCKED | No real model or target Windows hardware. Benchmark reports only tested local worker/SQL paths |
| Local docs and source archive | PASS | Reviewed documentation, verified source ZIP hashes and ZIP integrity |

## Critical release gates

Before any version is called a production Windows application: run CI and resolve real Rust/TypeScript/worker bundle build failures; validate setup/install/upgrade/uninstall in a clean Windows VM; prove worker shutdown and offline startup; test microphone/system-audio devices and audio-model accuracy; configure and test real Ollama/cloud providers with user consent; deliver a verified restricted code-execution service; security-review the local worker's unauthenticated loopback API, replace with authenticated IPC; and benchmark target CPU hardware. Generated artifact names are not installer evidence.
