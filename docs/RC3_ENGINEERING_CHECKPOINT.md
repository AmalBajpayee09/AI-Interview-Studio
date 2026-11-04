# AI Interview Studio v1.0 RC3 — Engineering checkpoint

## Canonical branch and preservation

Source of truth: `feature/v1.0-rc3-production-acceptance` based on RC2 `dab3130f253fb0620df3a8eb8e8d817692f485a3`. Production `main` is unchanged. See `RC3_RECOVERY_CHECKPOINT.md` for baseline/source comparison. Review in Draft Pull Request #11. Any exact RC3 commit, source ZIP SHA and Windows acceptance result must be taken from the completed Actions workflow, not assumed from this document.

## Changes

1. Fixed a real SQLite migration bug: on fresh databases the earlier `ai_usage` migration executed after v7 setup and reset `PRAGMA user_version` to 6. AI-usage schema now initializes idempotently without altering the version marker. Existing session records and legacy quiz data are preserved.
2. Added completed-assessment result retrieval (limited to attempts with persisted receipts). Unfinished attempts cannot retrieve answer keys from this API. The React desktop has a **Review last result** action visible when a completed attempt exists.
3. The worker now returns authoritative server wall-clock and deadline data from assessment start; the UI uses `performance.now()`-anchored countdown rather than a user-adjustable wall clock. Actual submission/late-save rules remain enforced by backend SQLite/API.
4. Added API/migration regression tests and a real authenticated Python worker subprocess test across three process lifetimes; original legacy API and data contracts remain supported.
5. Introduced a Windows test-only Playwright CDP harness to automate the **actual installed** Tauri WebView2 UI. The test creates a synthetic assessment through UI, saves answers, exits and relaunches the desktop, restores the original attempt and score, and reviews the persisted result after another relaunch. Debugging is opt-in in the isolated test process; not enabled by the production app itself.
6. Bumped all supported frontend/worker/Rust release metadata to `1.0.0-rc.3`. Fixed the native health-check regression fixture that initially expected the old RC2 version.

## Evidence / status

- Before changes, local canonical-source baseline: Python 112 passed / 13 skipped / 0 failed (Linux).
- After changes, **117 passed / 13 skipped / 0 failed** (Linux Python 3.13), including 5 focused RC3 tests and a real subprocess restart/SQLite recovery scenario.
- React compilation, Rust checks, NSIS and installed desktop/WebView2 results are **not** established by this local environment. Read the final exact-commit Windows CI conclusion and step logs; if a test fails, release acceptance fails.
- No real local Ollama service, consented cloud key, Docker Desktop or Windows microphone device is accessible to this Linux development host.

## Release decision

**RC3 ENGINEERING CHECKPOINT — NOT PRODUCTION READY** until full installed UI, provider inference, Docker Desktop, real audio and resumed-session acceptance all pass. A compiled installer is not sufficient.
