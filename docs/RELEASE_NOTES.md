# Release notes

## Source preview v0.3.0 — incremental engineering update

This release preserves the v0.2 SQLite schema and existing AI interview workflows. It adds authenticated bundled-worker source, optional Docker-isolated code execution, experimental audio device capture with source-separated transcripts, React controls, and expanded unit tests. A genuine Windows installer, completed diarization, real AI provider integration and fully verified frontend build remain blocked. Evidence and instructions: `IMPLEMENTATION_AUDIT_V03.md`, `RELEASE_GATE_V03.md`, `WINDOWS_RELEASE_V03.md`. No Windows `.exe` was created.

# Source preview v0.1.0 — 2026-11-01

Initial source distribution containing React/Tauri desktop project, Python FastAPI worker and tested browser companion, SQLite sessions/assessments and uploads, model adapters, optional STT endpoint, beginner PowerShell setup/build workflows, automated Python tests and honest performance measurements.

Not a general-availability Windows installer. Windows packaging, frontend compilation and real inference/STT benchmarks require an actual compatible Windows development machine and model/provider setup. No updates/signing/secure browser bypass features are delivered.

## Source preview v0.2.0 — completion add-on (2026-11-02)

- Audited existing source against 22-page completion add-on.
- Added read-only SQL training dataset, SQL editor in both interfaces, SQL authorizer, timeout and response caps.
- Added persistent assessment drafts, answer recovery and server-side question validation; SQLite migration v3.
- Added transactional SQLite backup endpoint and CLI restore after integrity verification.
- Added resource-mode storage/memory-pressure reporting (advisory, not active model scheduler); migration v4.
- Changed optional STT response to include segment timestamps and explicitly `unknown` speakers.
- Corrected PyInstaller data inclusion for browser companion assets; included experimental Windows CI workflow.
- Expanded Python tests; see `TEST_REPORT.json` for actual counts and test environment.

**Not shipped:** Windows `.exe` installer or portable binary; fully functional two-speaker STT, restricted code execution, real provider benchmarks, compiled React or Rust binaries. See `ADDON_COMPLETION_STATUS.md`.
