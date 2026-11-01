# Existing implementation audit — v0.1.0 baseline

Source reviewed: uploaded `AI-Interview-Studio-Source-v0.1.0.zip` (65 files); requirements: `addon.pdf` (22 pages) and original specification (58 pages).

| Subsystem | Audited state | Evidence / risk |
| --- | --- | --- |
| Python/FastAPI worker | Existing, runnable on this Linux host | `/api/health`, sessions, assessments, documents, AI adapters, `/api/transcribe` upload |
| SQLite | Functional local transactions with schema v2 | No draft persistence/backup at baseline; `connect` enables WAL and FKs |
| Ollama and cloud models | Implemented HTTP streaming adapters, real provider integration unverified | No Ollama service or credentials available for external integration tests |
| React/Tauri | Source exists, but not compiled in original delivery | No Rust compiler on host, dependencies unavailable offline |
| Standalone browser companion | Served by FastAPI | Usable without Tauri; does not replace a Windows installer |
| Audio | Upload-transcription integration exists with optional `faster-whisper` | Optional model missing; no continuous two-source capture or speaker diarization |
| Code | Python AST parser, not a runner | No isolated code execution backend; do not execute user code in worker process |
| MCQ/assessment | Scoring, timers, answer-key secrecy before submission | No server-backed draft autosave; UI uses client clock (non-proctored) |
| SQL | AI coaching prompts only | No executable practice SQL workspace |
| Local security | Loopback bind and browser Origin restrictions | Loopback HTTP can be called by local processes; dev companion deliberately unauthenticated |
| Installation | Windows source build scripts exist, installer not generated | Python worker bundling must include static assets; Windows build needs clean Windows VM |
| Overlay | Visible compact Tauri command | Never tested on Windows; does not bypass secure browsers or hide from monitors |

## Implementation approach

Keep working endpoints and backwards-compatible DB tables. Extend via versioned migrations, add read-only SQL sandbox with SQLite authorizer and runtime limits, persist timed assessment drafts and restore them, strengthen validation, expand tests, repair packaging static assets and document release limitations. No claimed Windows installer without actual Windows compilation/testing.
