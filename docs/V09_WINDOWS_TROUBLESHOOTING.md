# Windows startup and provider troubleshooting (v0.9)

| Symptom | Evidence to check | Resolution |
|---|---|---|
| Desktop reports `launch_failed` | `worker-lifecycle.jsonl`: `worker_spawn/error` | Reinstall using matching Windows x64 installer. Check antivirus quarantine and installation folder permissions. |
| `waiting_for_authenticated_health` times out | Worker `worker-startup.jsonl`, `worker-stderr.log` (private) and `worker-readiness.json` | Check port-blocking security software; confirm the worker process survives. Do not disable security tools blindly. |
| `restart_exhausted` | `restart_attempts` and `failure_category` | Export diagnostics from the desktop warning, retry once, then inspect private worker stderr locally. |
| `health_lost` after previously ready | Supervisor health-loss event, process liveness | Worker hung or closed its port; automatic recovery is bounded to two retries. |
| Database fails initialization | Worker event `database_failure` | Check `%USERPROFILE%\.ai-interview-studio` writable location, disk space and SQLite integrity. Back up the database before restoring. |
| Ollama unavailable | `/api/providers/status`, local Ollama `/api/tags` | Install/start Ollama and pull a model, then select its exact name. Internet is not required for local inference after the model is installed. |
| Model not found | `/api/models` list | Choose a downloaded model rather than an arbitrary name. |
| Cloud provider unavailable | Cloud consent/key status | Cloud is optional; do not enable to fix local Ollama startup. |
| Diagnostic export fails | Desktop worker lifecycle log | Ensure app local log directory exists and is writable. |

In Windows, the Tauri app log directory is normally beneath the current user's local app data. Select **Export diagnostics** in the application's offline warning to obtain the exact export path. Shared exports intentionally omit raw worker stderr, credentials, session contents, token, audio and resume content. The private `worker-stderr.log` remains local for troubleshooting and is not automatically uploaded.

Run the exact release's GitHub Actions installer smoke test and compare its `worker-readiness.json` authenticated marker to the installed desktop process; a mere running `.exe` is insufficient.
