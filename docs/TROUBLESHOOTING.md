# Troubleshooting — diagnosis, repair and verification

Open PowerShell in the project directory and run `./scripts/diagnose.ps1` to get a local environment report. Never paste secrets, API keys or complete resumes into public issue trackers.

| Error | Why it happens / how to confirm | Fix and how to check it |
| --- | --- | --- |
| `py` or Python not found | Python launcher absent or 3.11 not installed; `py -0p` lists versions. | Install Python 3.11 from python.org, reopen PowerShell, run `py -3.11 --version`. |
| venv missing or activation blocked | `.venv\Scripts\python.exe` absent; PowerShell policy may block `Activate.ps1`. | Run `py -3.11 -m venv services\ai_worker\.venv`; call the full venv Python path directly. Check `...\.venv\Scripts\python.exe --version`. |
| ModuleNotFoundError | Python packages were installed outside the worker virtual environment. | Run `...\.venv\Scripts\python.exe -m pip install -r services\ai_worker\requirements.txt`; rerun tests. |
| Worker offline / connection refused | Port 8765 service not started. Check `Invoke-RestMethod http://127.0.0.1:8765/api/health`. | Start `scripts/run-browser.ps1` or `scripts/dev.ps1`, then repeat health request. |
| Port already in use | Another service owns 8765. Run `Get-NetTCPConnection -LocalPort 8765` and inspect owning PID. | Close duplicate Studio worker; do not randomly kill unrelated programs. Retry health. |
| `node`/`npm` not found | Node LTS missing. `Get-Command node` fails. | Install Node LTS from nodejs.org, reopen terminal; run `node --version` and `npm --version`. |
| `npm install` fails | Network, proxy, DNS or dependency lock mismatch. Check output and `npm config get registry`. | Restore network access to official registry; run `npm install` in `apps/desktop`. Check that `node_modules` exists, then `npm run build`. |
| Rust / Cargo not found | Rustup not installed or PATH outdated. Check `rustc --version`. | Install Rust MSVC using rustup, reopen shell, run `cargo --version`. |
| Missing Visual C++ toolchain / Windows SDK | Linker fails during Tauri build. | Install Visual Studio C++ Build Tools with Desktop development with C++ and Windows SDK. Repeat `cargo test` in `src-tauri`. |
| WebView2 missing | App window won't initialize on older Windows installations. | Install Microsoft Evergreen WebView2 runtime; reopen packaged app. |
| Worker PyInstaller failure | Hidden library/dynamic import, unavailable wheel or memory pressure; review `build` output. | Try `py -3.11` venv, upgrade pip and reinstall pinned dependencies; run worker alone before packaging. Inspect produced `.exe` with `--help` only if supported. |
| Local AI unavailable | `ollama list` fails / `/api/tags` not reachable. | Install/run Ollama and pull model explicitly, then check `Invoke-RestMethod http://127.0.0.1:11434/api/tags`. |
| Model not found / memory exhausted | Model tag wrong or too large. Compare `ollama list` and available RAM in Task Manager. | Set `.env` model to an existing smaller one; restart worker and retry. |
| Slow local AI | Model too big, CPU-only backend, long context. | Use a smaller model and short mode; measure actual end-to-end time, not guessed GPU acceleration. |
| Cloud 401, 429 or quota | Invalid key, model entitlement, rate limit or billing restriction. | Verify local `.env` and account access without printing key; wait for quota/reconfigure; disabled cloud still allows offline quiz. |
| Cloud timeout/network error | Provider unreachable or network blocked. | Check internet and status of your provider; use local inference if installed. Retry only when connectivity returns. |
| Mic denied / missing | Permission not granted or unavailable device. | In Windows Settings → Privacy → Microphone enable access, check browser/WebView permission, retry Record. |
| Transcription 503 | Optional `faster-whisper` not installed. | Install `requirements-stt.txt`, restart worker; verify using a consented short audio sample. |
| Inaccurate Hindi/Hinglish transcript | Lightweight multilingual STT model lacks accuracy, noise or domain terms. | Manually edit transcript, test a larger supported model or better mic. Do not assume perfect recognition. |
| OCR 422 / missing Tesseract | OCR engine missing or image unreadable. | Install Tesseract OCR on Windows, verify `tesseract --version`, use high-contrast image and inspect extracted text. |
| PDF/DOCX extraction 422 | Damaged/scanned/password-protected file. | Try an unencrypted text PDF or OCR images, check file limits (6 MB, 100 pages). |
| SQLite migration failure | DB unwritable, disk full, corrupted user directory. | Check disk permissions and free space; backup DB, run a clean test with `STUDIO_DATA_DIR` pointing at a writable folder. Never delete existing user data blindly. |
| Crash/renderer blank | Node dependencies missing or JS/runtime error. | Run `npm run build`, inspect Tauri console, verify API health; check event logs for Windows app errors. |
| Installer fails | Native toolchain not verified, unsigned installer, missing worker resource. | Rerun `scripts/build.ps1` and inspect NSIS output; test only on a dedicated machine before wide deployment. |
| Display scaling or multiple monitors | OS DPI and window layout differences. | Check Windows Display → Scale and screen arrangement; resize/reposition visible window; run a documented manual UI test. |
| Secure browser denies overlay | Kiosk policy intentionally blocks other apps. | Use a normal mock-practice environment or organizer-authorized configuration instead; do not disable monitoring/security controls. |

**Confirmation rule:** a fix counts only when its original failing operation runs again successfully. Tests run elsewhere do not imply this particular Windows machine is verified.
