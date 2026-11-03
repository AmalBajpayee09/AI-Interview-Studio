# v1.0 RC1 engineering checkpoint

**Status: NOT PRODUCTION READY.** Focus: server-owned timed assessment and grading integrity while preserving legacy practice.

## Changes
1. Add non-destructive SQLite v6→v7 columns `require_start`, `negative_marking`, `cutoff_pct`. Old rows keep legacy defaults and data.
2. Newly created strict assessments require a persisted server-issued start. The client cannot forge the clock or delete a strict draft to reset it; deadline grading uses answers saved before expiry.
3. The backend stores grading penalty and overall cutoff, rather than accepting client penalty manipulation; results expose the cutoff result after submission.
4. Attempt receipt insertion and draft removal share a transaction. Duplicate retries return an identical receipt/result without increasing attempt counts.
5. React custom assessment form supports duration, penalty and optional cutoff; distinguishes server-timed from legacy practice.

## Verification
- Local Linux Python 3.13.5: 110 tests passed, 12 skipped, 0 failed; strict tests in `test_rc1_assessment_integrity.py`.
- Real localhost process smoke: packaged-*equivalent source worker* authentication, SQLite draft persistence after worker restart, grading, retry and secret-free startup log; `scripts/rc1_worker_acceptance.py`. NOT a Windows executable.
- TypeScript source syntax transpilation passed locally; real `npm ci && npm run build`, `cargo check`, NSIS and Windows packaged-worker API acceptance must be taken from the **final-commit GitHub Actions logs**.
- No live Ollama/cloud model, Docker Desktop, Windows devices or full native WebView assessment acceptance performed.

## Remaining high-priority gates
Windows install / re-install / upgrade and data retention, native worker readiness and recovery under failure, real local inference, cloud consent/credentials, Windows Docker Desktop isolation, real microphone/loopback plus qualified diarization, full mixed-format timed UI assessment, resume-grounded interview and analytics, target hardware performance, complete security review.

**Release policy:** Do not relabel an older 0.9.0-versioned NSIS artifact as a v1.0 release. Do not merge this RC branch into main before the mandatory acceptance suite passes.
