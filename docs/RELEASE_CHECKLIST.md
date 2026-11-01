# Release checklist — source preview v0.2.0 (2026-11-02)

- [x] Read original 58-page PDF and retain copy as project reference.
- [x] Inspect the supplied Safe Exam Browser ZIP without running it or patching security-critical code.
- [x] Create Python worker, SQLite migrations, local HTTP API, model adapters, assessment and text analysis services.
- [x] Create React + TypeScript UI source and Tauri 2 Rust shell source.
- [x] Create dependency-free browser companion as a runnable fallback.
- [x] Create PowerShell setup, test, diagnose, dev and attempted installer build recipes.
- [x] Execute Python API unit/integration tests successfully in Linux container.
- [x] Capture real microbenchmark output from this container in `BENCHMARK.json`.
- [x] Document supported feature status and release limitations.
- [ ] Run React TypeScript build (`npm` registry DNS unavailable here).
- [ ] Run Tauri Rust compilation and tests (`cargo` absent here).
- [ ] Run production PyInstaller worker bundling on Windows.
- [ ] Produce and validate actual Windows NSIS installer.
- [ ] Run a clean Windows 10/11 install and native E2E tests.
- [ ] Test real Ollama/cloud model generation on target hardware.
- [ ] Test mic/STT pipeline and audio-to-answer latency on target hardware.
- [ ] Test OCR, document parsing and file handling on Windows.
- [ ] Validate Windows overlay capture behavior with authorization.
- [ ] Upgrade key storage to Windows Credential Manager / authenticated IPC.
- [ ] Conduct dependency audit, reproducibility checks, signing and packaging verification.

**Release decision:** Source preview only. NOT a production-ready, complete implementation of every demand. Do not distribute as a proven Windows installer.

Additional checks executed on the source preview:

- [x] 32 automated Python tests passed after latest origin and concurrency fixes.
- [x] TypeScript/TSX source syntax transpiled (8 files, no syntax diagnostics); **not** a type-check or build.
- [x] Dependency-free companion inline JavaScript passed Node `--check`.
- [x] Real localhost HTTP GET `/api/health` returned 200, and browser HTML returned HTTP 200.
- [x] Text extraction and Linux Tesseract OCR smoke checks returned 200 (OCR concatenated two words, confirming extraction is imperfect).
- [ ] Chromium headless screenshot smoke (process hung due container display/DBus limitations; no screenshot verified).

## Completion add-on work performed (2026-11-02)

- [x] Source and add-on audited in `IMPLEMENTATION_AUDIT.md`.
- [x] Read-only SQL fixture + authorizer with real HTTP SQL endpoint verified.
- [x] Assessment draft save/recovery and quiz validation; schema migration v3.
- [x] Persistent advisory resource modes and memory sampling; schema migration v4.
- [x] SQLite backup endpoint + offline validated restore utility.
- [x] Timestamped STT response contract checked with mocked decoder (no real model benchmark).
- [x] 32 Python tests passed on Linux (pytest), including migration from original v2 schema.
- [x] Five real HTTP smoke tests passed on localhost.
- [x] Inline companion JavaScript and 8 frontend TS/TSX files passed syntax parsing/transpilation.
- [ ] React production build — missing npm dependencies and registry DNS.
- [ ] Native Tauri Rust compilation — Cargo and Windows toolchain unavailable.
- [ ] Headless Chromium interaction — blocked by environment browser policy (`ERR_BLOCKED_BY_ADMINISTRATOR`).
- [ ] Windows installer and portable EXE — not produced; Windows CI workflow provided but unrun.
- [ ] Real continuous dual speaker capture, OS sandbox, model inference and Windows overlay validation.

Release gate remains **NOT SATISFIED**. Refer to `ADDON_COMPLETION_STATUS.md`.
