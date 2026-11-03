# RC2 acceptance and blocker register

| Acceptance item | Evidence level | Exact blocker / next action |
|---|---|---|
| Python worker suite | Local Linux 110 pass, 12 skip, 0 fail on prerelease snapshot | Repeat on exact branch in CI; skip != pass |
| React/TypeScript + Rust/Tauri | Windows RC2 CI configured; no unverified success claim | Run .github/workflows/windows-release.yml |
| Windows NSIS clean install | Real RC1 success in [41683032273](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41683032273) | RC2 exact-commit installer must pass separately |
| Windows real in-place upgrade | **New strict RC2 script, not yet accepted** | Download RC1 artifact #13255325662, verify SHA-256 6EECCB4E59F3D59069AF44B6565B374F094F370693C24C0704988901B54026B8, install, upgrade and verify |
| Worker crash and no orphan | New script kills owned process tree and polls authenticated marker for new PID | Must pass on Windows; parent-only kill and possible orphaned child not tested |
| SQLite data | v7 migration and draft receipt unit/API tests | RC2 tests pre-upgrade session preservation through actual installer |
| Timed assessment UI | New ordered saves and one-shot auto-submit; 110 baseline API tests | Installed WebView restart/timeout/navigation acceptance untested |
| Genuine Ollama | BLOCKED: no Ollama service/model in current container | Explicit live test with downloaded model and recorded TTFT |
| Genuine cloud provider | BLOCKED: user consent and valid test credentials unavailable | Windows Credential Manager + opt-in real service test |
| Windows Docker Desktop | BLOCKED: no Docker Desktop Windows engine | Run genuine container/attack tests on supported Windows |
| Windows audio/diarization | BLOCKED: no accessible microphone/loopback/reference recordings | Test real consented devices and known-speaker fixtures |
| Resume → mock interview | PARTIAL: extraction API and local context implemented | Test PDF/DOCX in UI through real model and analytics |
| Security acceptance | PARTIAL: scoped review below | Third-party code/dependency audit, code signing, Windows sandbox verification |
| Target laptop performance | BLOCKED | Report real PC hardware/OS, CPU, RAM, model, data, p50/p95 |

The exact RC2 Windows script is `scripts/rc2-windows-acceptance.ps1`. A **passing** GitHub runner reports: previous installer hash, clean install, old SQLite session, in-place upgrade, authenticated worker after recovery, no worker after shutdown, relaunch, silent uninstall and data retention. A failure must fail the step and must not be relabelled as acceptance.

The script does **not** verify all WebView controls, full interview conversation, actual AI provider, Docker Desktop, audio hardware or rollback. Those gates must be tested separately. Never claim release accepted until all mandatory gates pass.
