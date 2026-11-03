# v0.9 Windows worker-startup investigation and resolution

## Evidence, not assumptions

- v0.7 final-commit run `41486713650` failed **after native compilation**, in its installed-desktop smoke step: `Bundled Python worker not started`. That runner did not establish the root cause, so do **not** equate the failure with a proven PyInstaller or resource-resolution defect.
- v0.8 canonical commit `3d428cbb23d99e98cd00c9a94187ac71881adae7`, run `41496591667`: all listed job stages succeeded, including standalone bundled-worker authenticated health, Windows installer packaging, installed desktop and worker process observation and SQLite creation. This demonstrates v0.8 improvement, but its installed smoke test used an **unconditional 12-second sleep** and only observed the worker process, not the authenticated application-to-worker handshake.
- Local v0.9 Python subprocess tests exercise real loopback HTTP token authentication, database initialization, shutdown and restart; they do not run the Windows Rust shell.

## v0.9 lifecycle design

1. Tauri resolves its packaged worker from the configured Tauri resource directory (with OS path APIs rather than shell quoting) and creates a per-launch random loopback port and token.
2. A dedicated supervisor starts the bundled executable with its installation directory as its working directory. Process-specific `STUDIO_PORT`, `STUDIO_WORKER_TOKEN` and `STUDIO_DIAGNOSTIC_DIR` variables are inherited only by its worker, not stored in a plaintext file.
3. The worker initializes and migrates SQLite inside FastAPI lifespan, writing allowlisted startup events.
4. The Rust supervisor connects to `127.0.0.1:<port>` and sends a local authenticated HTTP GET to `/api/health` with the token; it only declares `ready=true` if the response has HTTP 200, `status=ok` and an exactly matching worker version.
5. A nonblocking Tauri IPC `worker_connection` waits for this handshake before returning an IPC connection to the frontend. An authentication failure or timeout cannot masquerade as a successful startup.
6. Supervisor checks process liveness and periodically re-probes health. Process exits, health loss and startup timeouts trigger up to **two** automatic restarts after the initial spawn. A manual restart resets the budget.
7. When all attempts fail the UI offers manual retry and user-accessible, allowlisted diagnostic export. The UI can display the worker's stage instead of blindly assuming ready.
8. Shutdown terminates the owned process tree on Windows via `taskkill /PID <owned-pid> /T /F`, with a direct child kill/wait fallback.

Polling every 200–300 ms is used to **check an actual authenticated readiness condition**, not as a fixed startup-delay substitute. The Python worker's own structured events and the Rust `worker-readiness.json` marker contain no token, credentials, prompts, transcript, source document text or recorded audio. Logs are rotated by size, with a bounded previous generation.

## Status at source packaging

- Python real process / auth / SQLite / process restart: **PASS on Linux**.
- Tauri supervisor build, authenticated desktop handshake and bounded restart: **NOT VERIFIED on Windows** until a successful v0.9 CI run and published logs.
- v0.9 installer launch and SQLite restart: **NOT VERIFIED** until the exact v0.9 artifact passes the Windows acceptance job.
- Database upgrade from v0.8: **NOT VERIFIED**; a clean install/restart is not an upgrade test.
- Headless GitHub Actions tests do not constitute a physical user-device acceptance test.
