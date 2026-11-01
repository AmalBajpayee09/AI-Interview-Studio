# Developer guide

Keep changes modular; endpoints live in `services/ai_worker/app/main.py`, SQL authorizer in `sql_lab.py`, SQLite migrations in `db.py`, provider adapters in `providers.py`, and React views under `apps/desktop/src/views/`. Both browser companion and React interface call the loopback worker. The native app has only narrowly scoped Tauri commands.

## Local Python checks

```powershell
$env:PYTHONPATH='services/ai_worker'
.\services\ai_worker\.venv\Scripts\python.exe -m pytest services\ai_worker\tests -q
```

Use `scripts/test.ps1` on a fully provisioned Windows developer machine to additionally run npm build and cargo test. In offline environments, native compilation is **not** validated merely by TS syntax transpilation.

## Windows release experiment

Run `scripts/build.ps1` from the repository root on Windows with Node, Rust, C++ Build Tools, Python 3.11 and package registry access. It builds PyInstaller worker resources then invokes Tauri NSIS. The GitHub Actions workflow `.github/workflows/windows-release.yml` can be run manually after pushing the project to an authorized GitHub repository. Workflow success does not replace testing install/upgrade/uninstall on clean Windows VMs.

**Critical open issues:** Worker HTTP is loopback-only but unauthenticated; production needs authenticated IPC. Code is parsed but never run; no secure OS sandbox is available. Audio is segment upload STT, not live two-speaker streaming. Credentials must remain in environment local files until Windows Credential Manager integration is implemented.

## Database schema

Versioned through `PRAGMA user_version=4` and idempotent migrations in `db.initialize()`: v1 sessions/turns/documents/assessments/attempts, v2 indexes, v3 `assessment_drafts`, v4 `settings`. Use SQLite online backup before altering schema. Never delete user databases to resolve a migration issue.
