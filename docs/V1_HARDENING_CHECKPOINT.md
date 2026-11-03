# v1.0 acceptance-hardening checkpoint — NOT PRODUCTION-READY

This is a security and reliability increment on top of the canonical v0.13 development branch. It is **not** a finished v1.0 release or a verified installer. All original 130 requirement IDs are preserved.

## Milestone evidence

- v0.10: genuine Linux Docker four-language / isolation tests passed in GitHub Actions run [41650879175](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41650879175), commit `9c93ee2bd768f46e7e245a36604f67942725b7d8`. This does not validate Windows Docker Desktop.
- v0.11: offline 16-bit PCM WAV channel and activity tests exist. Windows microphone, loopback, real STT and diarization acceptance remains unavailable.
- v0.12: recoverable server-start drafts and transactional duplicate-submission receipts exist; full exam timing and schema coverage remain incomplete.
- v0.13: source-backed resume sections and project prompts were corrected; GitHub Windows validation [41651936422](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41651936422) passed Python tests, React build and Rust checks. Not a full resume mock-interview acceptance.

## This checkpoint: actual changes

1. Existing active assessment drafts have immutable server-saved start times. A client-supplied different timestamp returns HTTP 409.
2. Autosaves after the recorded assessment deadline return HTTP 409. A late submission is scored from **previously autosaved** answers, never newly submitted answers. Duplicate receipt behavior remains intact.
3. The assessment results view discloses timeout handling and explicitly labels legacy direct submissions as unstarted practice.
4. Stereo WAV activity detection uses per-channel signal energy rather than summing channels before squaring. Two equal and opposite signals do not cancel into false silence. Speaker identity is never inferred from this test.

## Tests genuinely run

On Linux Python 3.13.5, `PYTHONPATH=services/ai_worker pytest -q services/ai_worker/tests --disable-warnings --tb=short`: **106 passed, 12 skipped, 0 failed, 1 warning**. The new module `test_v1_acceptance.py` supplies four unit/API/audio-fixture checks. Python compileall and TypeScript syntax transpilation passed locally; those checks are not native Windows compilation or full UI validation.

## Security/reliability limitations

- Legacy direct assessment submissions without a server-start draft are retained for backward compatibility and explicitly marked `legacy_unstarted_practice`. They are **not secure timed exams**.
- Candidate-specified negative marking, trusted server deadlines through restarts, explicit timeout auto-finalization when a worker is closed, and full schema/cutoffs are unfinished.
- WAV energy detection is not speech recognition, speaker diarization or a Windows audio-device acceptance test.
- Real Docker integration was validated on Linux in the earlier v0.10 milestone; no Docker engine is available on the local sandbox. Windows Docker Desktop acceptance remains outstanding.
- Real Ollama/cloud inference, production Windows clean install + upgrade, full security audit, and target-hardware performance remain unverified in this checkpoint. No new v1.0 installer or performance claims.

## Required next release checks

Run the updated branch on Windows with locked npm dependencies, Python regression, Rust tests, build the actual installer and verify worker start/auth/readiness; conduct an interactive exam restart/timeout acceptance; test genuine provider inference, Docker Desktop, and consented audio on supported hardware; perform upgrade/uninstall and retention checks. Only promote requirements with exact recorded evidence.
