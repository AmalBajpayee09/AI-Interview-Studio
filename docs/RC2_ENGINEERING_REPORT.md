# v1.0 RC2 engineering checkpoint — source-of-truth, progress and release gate

Canonical baseline: `feature/v1.0-rc1-timed-assessment-integrity` at `8ea4a39de9a1afa8b0b1a830aa96ad34fe7eda33`; current integration branch: `feature/v1.0-rc2-windows-acceptance`. Production `main` remains at `b4a9d2b449122a29fa7b874652473648e9384f05`, untouched. Inspect branch HEAD for the final SHA; the submitted engineering ZIP is not a substitute for the Git commit.

Uploaded RC1 ZIP: 195 source members, CRC passes, SHA-256 `106a77dc7623c92c94cf87d03bc8717c7554373d09197a4672bbd28d6da7e44f`. Local ZIP differed from GitHub for backend/database/workflow, so GitHub RC1 was selected as canonical; newer GitHub provider, credential and worker logic was not overwritten.

Architecture preserved: React/TypeScript/Vite frontend, Rust/Tauri supervisor, FastAPI Python worker, per-launch local auth and SQLite migration v7, provider adapters, Docker sandbox runner, opt-in audio, assessment UI and resume intelligence.

Changes implemented: `1.0.0-rc.2` prerelease version consistently across desktop/frontend/Python/tests; serial frontend autosaves and a one-shot automatic deadline submit to reduce race/duplicate requests; Windows NSIS upgrade acceptance harness that verifies the real previous installer SHA, installs into a Unicode path, checks worker readiness, session data retention, process-tree crash recovery, restart and uninstall.

Baseline local test: `PYTHONPATH=services/ai_worker python -m pytest services/ai_worker/tests -q`: **110 passed, 12 skipped** (uploaded RC1 + prerelease backend/UI changes). Frontend TypeScript syntax transpilation passed locally; full React/Rust/native and installed-app checks are GitHub Windows CI only. Previous RC1 real installer+installed worker acceptance **passed**: [run 41683032273](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41683032273). RC2 outcome must be read from the exact final commit, not inferred.

Requirement matrix: **157 IDs**, the original 149 unchanged plus 8 RC2 gates. Current counts: {"PARTIALLY IMPLEMENTED":81,"NOT IMPLEMENTED":24,"TESTED — DEFINED CODE-PATH":20,"INTEGRATION TESTED":13,"BLOCKED":15,"UNIT TESTED":4}. No original requirement was promoted on mock-only evidence.

Release decision: **RC2 ENGINEERING CHECKPOINT / NOT PRODUCTION-READY** until Windows upgrade, real model, Docker Desktop, audio and end-to-end user acceptance are evidenced. See RC2_ACCEPTANCE_AND_BLOCKERS.md and RC2_SECURITY_AND_PERFORMANCE.md.
