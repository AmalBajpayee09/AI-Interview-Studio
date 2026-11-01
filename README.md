# AI Interview Studio v0.4.0

AI-assisted Windows desktop application for **authorized mock interviews and assessment practice**. Built with Tauri 2, Rust, React/TypeScript, a bundled Python AI worker, and SQLite. This repository preserves functionality from v0.1 through v0.3 and adds incremental v0.4 improvements.

## Actual Windows release evidence (2026-11-02)

- **Windows application and NSIS installer:** generated successfully by [Windows CI run 41347725338](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41347725338). The installer was downloaded and independently SHA-256 verified (`bfcdeb9d232e4bd02119bdc5b39f0913f1421607334ee07a65116a6eacbdc8f9`).
- **Windows build tests:** Python 51/51 tests passed, real `npm ci` and React/TypeScript production build passed, Cargo check and tests passed, and the Python worker was packaged via PyInstaller.
- **Installed desktop smoke test:** [Windows run 41349033077](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41349033077) passed silent NSIS installation, detection of installed desktop+worker, desktop launch with worker running, and a silent uninstall attempt.
- **Portable launch smoke test:** [Windows run 41349336117](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41349336117) passed extracting the portable distribution and launching its desktop app with a running worker without installing.
- A separate **cleaned portable ZIP** contains only `ai-interview-studio.exe` and `ai-studio-worker.exe`. Installer and portable downloads are attached in the ChatGPT project conversation. GitHub workflow artifacts are available via the CI run links.

**Scope:** This is an actual compiled Windows installable *preview*, not a claim that every specification feature is production complete. End-to-end real Windows audio, robust speaker diarization, full GPU/memory optimization, physical baseline-hardware benchmarks, real Ollama/cloud calls and Docker execution still need validation. The Windows installer is unsigned; users should verify the SHA-256 and only install from a trusted source. See [current release gates](docs/V04_RELEASE_GATE.md) and [Windows CI evidence](docs/V04_WINDOWS_CI_RESULTS.json).

## Included modules

- **Interview practice:** persistent sessions and follow-ups, answer modes, streamed provider adapters, context from user-supplied projects and resumes, session export/deletion.
- **Assessments:** timed practice, MCQ scoring and feedback, marking for review, persisted assessment drafts and recovery.
- **SQL lab:** isolated read-only sample database, query validation and bounded timeouts, result tables and JOIN/aggregation support.
- **Coding practice:** static syntax analysis plus optional Docker-only execution for Python, C++, Java and JavaScript, sample and custom test cases, output/timeout controls, per-language draft recovery. Code execution is **disabled** unless a suitable Docker runtime is installed; there is no unsafe host execution fallback.
- **Audio:** opt-in experimental microphone/system-source capture, pause/resume, bounded buffering, optional locally configured transcription, timestamped events. Mixed-speaker diarization and reliable attribution are not yet complete; unknown labels are used as needed.
- **Resume/communication/analytics:** local PDF/DOCX/text/OCR ingestion where dependencies allow, project-context retrieval, text-based speaking feedback, historical session analytics.
- **Data/security:** SQLite migrations, backups and offline restore, optional cloud inference requiring consent and configuration, authenticated desktop-to-worker communication, local retention controls.

The original 58-page specification and prior add-on are retained as local documentation in the **downloadable source ZIP**, but excluded from the public GitHub repository. The Safe Exam Browser third-party code is not packaged or modified to bypass exam/proctoring controls.

## Use the Windows installer

Download `AI-Interview-Studio-Setup-v0.4.0.exe` from the ChatGPT conversation and verify its SHA-256:

```powershell
Get-FileHash .\AI-Interview-Studio-Setup-v0.4.0.exe -Algorithm SHA256
```

Expected: `bfcdeb9d232e4bd02119bdc5b39f0913f1421607334ee07a65116a6eacbdc8f9`.

Run the installer, launch **AI Interview Studio**, and configure a local Ollama model if you want actual AI-generated answers. An installed application does not include model weights and does not require a cloud API key for basic offline features.

Alternatively, extract `AI-Interview-Studio-Portable-v0.4.0.zip` into a writable directory and run `ai-interview-studio.exe`; keep `ai-studio-worker.exe` beside it. Portable output is not a substitute for a signed managed installer.

## Developer setup

On a Windows development machine install Python 3.11, Node.js 22, Rust stable MSVC, Visual Studio C++ Build Tools and WebView2. See the [Windows setup guide](docs/WINDOWS_SETUP.md) and [developer guide](docs/DEVELOPER_GUIDE.md).

```powershell
# From the repository root:
cd apps\desktop
npm ci
npm run build
cd ..\..
.\scripts\setup.ps1
.\scripts\dev.ps1
```

Windows production compilation is tested via [GitHub Actions](.github/workflows/windows-release.yml); source builds call `scripts/build.ps1` to bundle the worker and native app. Python tests:

```powershell
$env:PYTHONPATH = 'services/ai_worker'
py -3.11 -m pytest services/ai_worker/tests -q
```

The development-only local browser companion is available via `scripts/run-browser.ps1`. Local Ollama instructions are in [LOCAL_AI_SETUP.md](docs/LOCAL_AI_SETUP.md); cloud configuration is in [CLOUD_AI_SETUP.md](docs/CLOUD_AI_SETUP.md).

## Architecture and privacy

React/Tauri UI → scoped Rust command / authenticated local worker API → Python worker → SQLite and user-chosen providers. The standalone browser companion uses local loopback access and should not be exposed beyond a trusted machine. Cloud inference is explicitly disabled by default. API keys are never included in the source archive or Windows binaries. OS credential vault integration and signed update distribution remain pending.

See [architecture](docs/ARCHITECTURE.md), [security notes](docs/SECURITY.md), [troubleshooting](docs/TROUBLESHOOTING.md), [v0.4 release report](docs/V04_RELEASE_GATE.md) and [test results](docs/V04_TEST_REPORT.json). Project source is MIT licensed. This application must not be used to bypass proctoring or recording restrictions.