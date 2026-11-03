# v0.9 release gate

**Current result: developer source, Windows native and live-provider acceptance PENDING.**

- Python 86 passed, 4 skipped. A real standalone worker starts, authenticates, initializes SQLite, restarts and recovers a session on Linux.
- Canonical GitHub v0.8 Windows baseline succeeded: run 41496591667 at commit 3d428cbb23d99e98cd00c9a94187ac71881adae7.
- v0.9 Rust supervisor uses authenticated health rather than fixed sleeps, has bounded recovery, lifecycle logs, user-export diagnostics and real readiness-state UI. **The new Rust code must compile and pass the v0.9 Windows workflow before becoming verified.**
- Ollama: offline/not installed in development host. Real inference and first-token latency NOT VERIFIED.
- Windows upgrade from v0.8: NOT VERIFIED.
- Security: tokens not written to logs or exports; Python events allowlist, log rotation; no code execution scope expansion.
- All 130 requirement IDs retained in `V09_FEATURES.json`; statuses preserved without unsupported promotions.
- Full install → real Ollama → follow-up → restart workflow: NOT VERIFIED. Production readiness NOT APPROVED.
