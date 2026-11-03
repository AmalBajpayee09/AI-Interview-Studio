# v1.0 RC1 source of truth — 2026-11-03

- Production main: `b4a9d2b449122a29fa7b874652473648e9384f05` (not modified).
- Parent development commit: `2e55beaa356a7b83ef12691f35e7dcbdf82ca3e5`.
- Canonical development branch: `feature/v1.0-rc1-timed-assessment-integrity`; use `git rev-parse HEAD` for the exact latest source commit.
- Earlier user-uploaded engineering ZIP: SHA-256 `fcef15ad84bcc78c8740fe6b1c196735b7e23322850f4d5d82f5a07bb21eb772`; this is NOT byte-identical to the GitHub development branch.
- Architecture: Tauri 2/Rust + React/TypeScript desktop; authenticated Python/FastAPI worker; SQLite migration v7; Ollama/cloud adapters; Windows vault; Docker code runner; audio/SQL/assessment/resume modules. Existing components preserved.
- Test baseline: Linux Python regression 110 passed, 12 skipped; real worker subprocess authenticated restart & SQLite assessment continuity passed. Windows CI is tracked separately and must be assessed at the **final commit**.
- 149 requirement IDs preserved (including original 130); changed RC1 statuses: F-07, F-09, V012-01, V100-03; see `REQUIREMENT_MATRIX.json`.
- Current release gate: **NOT PRODUCTION READY**. No live Windows audio, real provider inference, Windows Docker Desktop isolation, installed UI assessment recovery or upgrade acceptance proven in this cycle.
