# AI Interview Studio v0.8.0 — Integration hardening milestone

**Status: development branch, NOT production approved.** Base: uploaded v0.7 source; the GitHub `feature/v0.8.0-integration-hardening` branch is canonical because it preserves additional newer v0.7 provider retries, Windows credential management and AI-usage tracking not present in the uploaded ZIP. Do not overwrite the GitHub branch with the older uploaded source tree.

## Changes implemented

- In the Python worker, reject a second simultaneous generation for the same session with HTTP 409; cancellation discards incomplete responses; track measured first-token elapsed time for mock/live inference. Real provider measurements require a live model.
- In the Rust desktop process, provide worker status and an explicit authenticated restart path; write worker stderr to the user app log directory instead of discarding it. GUI recovery control wired into offline state. Worker token and cloud keys are never put in diagnostic messages by the Rust shell.
- Extend the Windows workflow with a standalone packaged-worker authentication/SQLite smoke test and a separate installed-desktop worker smoke. Build and installed-app validation are independent gates.
- Implement opt-in live tests for Ollama and cloud providers. They remain skipped unless explicitly enabled with credentials, consent and infrastructure.
- Expand Python/HTTP tests for cancellation, duplicate requests, persistence, sanitized errors and first-token metadata. Do not interpret mocked-provider test success as live AI success.

## Validation evidence

- Uploaded v0.7 archive baseline: 75 passed, 1 Windows-only skipped on Linux.
- New local v0.8 archive-based code: **80 passed, 3 skipped**, Python 3.13 Linux; Windows build **must be verified separately**. The skipped set is Windows Credential Manager, real Ollama inference, and real opt-in cloud inference.
- Real loopback worker subprocess (Linux): authenticated /api/health, unauthorized 401, persisted SQLite, 70 HTTP health measurements. See `V08_BENCHMARK.json`.
- At the time this document was first written: GitHub CI run is pending. Inspect GitHub Actions and exact commit for the current result; report failed stages honestly.

## Canonical source reconciliation

The uploaded v0.7 ZIP and GitHub's v0.7 development branch differ. GitHub has extra provider retry and usage tracking code. **The v0.8 GitHub branch preserves those changes**. The offline archive built from the user's uploaded source ZIP is therefore a testable reference snapshot, not automatically byte-identical to the GitHub branch. For the complete canonical tree, download the GitHub branch archive or the CI source archive artifact.

## Known remaining risk

- No real live Ollama model or authorized cloud provider tested in this environment.
- No Docker daemon or tested isolated code execution here; never execute untrusted code on host as fallback.
- No Windows microphones or actual diarization test environment available.
- Windows CI may build the desktop, but a successful compile is not equivalent to Windows worker launch, restart, upgrade and recovery acceptance.
- Native restart and logging commands are new and require actual Windows CI compilation and installed-app testing.
- Application and worker process shutdown does not yet guarantee all PyInstaller child-process descendants terminate on every Windows configuration.
- No guarantee that existing user-data upgrades from every prior installer version have passed.
- GUI is a visible, authorized practice workspace; no proctoring or capture evasion.
