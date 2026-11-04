# RC3 security findings, performance and remaining release blockers

## Focused security review (partial, not independent audit)

| Finding | Severity | Component | Change / remaining verification |
|---|---|---|---|
| Fresh initialization could downgrade SQLite schema marker 7→6 | Medium data-compatibility risk | Python SQLite migration | Fixed via unconditional idempotent `ai_usage` DDL with no schema downgrade; Linux tests on fresh and legacy databases passed. Confirm packaged Windows initialization in RC3 CI. |
| User-adjustable OS clock could shift displayed assessment countdown | Medium usability/integrity risk | React timer | Server-supplied deadline anchored to `performance.now()` for UI. Server still owns actual assessment deadline and accepts only saved answers after expiry. Windows clock-change test remains. |
| Completed assessment result not visible after app restart in assessment screen | Medium recovery/UX | API/SQLite + React | Added read-only completed-receipt endpoint and Review last result UI; Linux API and real worker subprocess evidence. Installed WebView2 test must pass before calling UI recovery verified. |
| Test-only remote debugging could expose renderer/worker token | High if accidentally enabled in production | WebView2 acceptance harness | Debugging port set only for isolated Windows CI child process; application does not enable by default. Do not run harness against real user profiles or network-accessible machines. |
| Local SQLite stores resume and session text in plaintext | Medium | Data directory | OS account permissions/backup hygiene; encrypted storage and robust deletion remain acceptance work. |
| Cloud environment key compatibility path remains | Medium | Provider credentials | Windows Credential Manager present, but legacy env variable fallback requires a targeted security review. |
| Untrusted code isolation only proven on Linux Docker | High | Docker runner | Windows Docker Desktop sandbox acceptance pending; no direct host execution fallback. |
| Installer unsigned | High deployment/reputation risk | Windows distribution | Code signing, reputation verification, rollback and independent dependency scanning are still required. |

No cloud keys, worker tokens, private prompts, audio or real resumes are included in the synthetic RC3 UI test or CI report. The WebView2 CDP loopback debug socket is only an automation feature in CI and should never be documented as a normal end-user setup option.

## Performance evidence

- Previous RC2 GitHub-hosted Windows Server 2025 runner reported a worker readiness sample after upgrade of **5,276 ms**, post-crash recovery sample of **4,831 ms**, and relaunch worker readiness of **4,417 ms**. Single samples, NOT median/p95 on a real user's laptop.
- RC3 Linux Python regression runtime is **11.71 seconds** for 117 passing tests + 13 skips; this is test runtime, not AI inference or application cold start.
- No real model generation or first-token timing is available; no target Windows memory/CPU, idle resource or audio latency metrics have been collected. Such benchmarks remain blocked.

## Explicit release blockers

Installed WebView2 timed-assessment acceptance pending exact-commit Windows CI; full timeout/system-clock and network-interruption scenarios not yet automated. Genuine Ollama inference, authorized cloud inference, Windows Docker Desktop, real microphone/system audio and multi-speaker diarization, resume-guided interview, third-party security review, code signing, update rollback, target-laptop performance, accessibility and display-scale testing remain incomplete.

Release status: **RC3 engineering checkpoint; NOT PRODUCTION-READY**.
