# Implementation roadmap — v0.5.0

This document is grounded in `FEATURE_COMPLETION_MATRIX.md`, not a guarantee of completion.

## Gate 0: source and repeatability

- Merge the v0.5 source and committed `apps/desktop/package-lock.json` to GitHub on a reviewed branch.
- Run Windows GitHub Actions (React production build, Rust checks, Python tests, PyInstaller/Tauri NSIS bundle) and download the *actual* artifact.
- Compare hashes; run a clean Windows install, launch, recovery, upgrade from v0.4.0, and uninstall test. **Not executed for v0.5.0.**

## Gate 1: safety-critical behavior

- Add Windows Credential Manager/OS secure secrets support and a migration path from local `.env` keys.
- Verify Docker containment under Windows Docker Desktop using actual malicious infinite loops, network attempts, filesystem attempts, and output floods. Disable execution if containment fails.
- Make localhost worker failure/restart handling and cancellation observable. Add dependency vulnerability scanning.

## Gate 2: core interview and assessment workflows

- Finish continuous question segmentation, manual/automatic triggers and cross-worker cancellation; test real Ollama + opt-in cloud responses with cost and latency measurements.
- Integrate the v0.5 single/multiple/numerical assessment UI into a compiled Windows build; add numeric tolerance UX, sectional timers and cutoffs.
- Add actual candidate answer evaluation and user-editable resume/project fact extraction; keep claims source-linked.

## Gate 3: speech, practice and analytics

- Test on the target Windows laptop using consented microphone and loopback devices; capture failures, latency and recoveries.
- Implement validated diarization based on actual recordings; unknown attribution remains mandatory when uncertain.
- Add syntax-highlighted multi-language editor, verified safe coding tests, SQL explanation and history, ML/HR/communication exercises.
- Derive analytics only from attempts and verified candidate activity; distinguish subjective feedback.

## Gate 4: production release

- Add multi-monitor and global shortcut QA, signed release/update strategy, long-running resource tests, auto-crash recovery, and a full end-to-end acceptance suite.
- Re-run and document the complete feature matrix after each gate. Do not label this build production-ready until all release-gate checks pass.
