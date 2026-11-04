# AI Interview Studio v1.0 RC3 — Release notes (engineering preview)

- Continues the verified RC2 architecture; `main` unchanged.
- Fixes fresh SQLite v7 migration ordering and idempotently repairs the AI-usage table.
- Improves timed-assessment countdown stability using the server's clock/deadline and a monotonic UI clock.
- Enables review of a completed assessment's persisted SQLite result after desktop relaunch.
- Adds genuine worker HTTP/SQLite restarts as regression tests and the first installed-WebView2 assessment automation harness.
- Aligns application/worker and Rust health metadata to `1.0.0-rc.3`.

**Not a production release.** Real model inference, Docker Desktop, Windows audio, full mock interview and security acceptance are not complete. Do not install on an exam machine or claim hidden recording capabilities. This version is for authorized practice only.

The installer and canonical source ZIP must be obtained exclusively from the exact-commit successful Windows CI run; no local development source ZIP should be passed off as a verified installer.
