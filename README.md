# AI Interview Studio v0.6.0 — development branch (not production approved)

AI-assisted Windows desktop application for **authorized mock interviews and assessment practice**. Built with Tauri 2, Rust, React/TypeScript, a bundled Python AI worker, and SQLite. This repository preserves functionality from v0.1 through v0.3 and adds incremental v0.4 improvements.


## v0.6 implementation and release status

- **Baseline:** v0.5.0 Windows installer, installed-app launch and packaging passed [v0.5.0 Windows smoke CI](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41448935263). These historical artifacts **do not validate v0.6**.
- **v0.6 additions:** Windows Credential Manager integration for OpenAI key storage (desktop Settings), opt-in cloud-consent toggle that overrides legacy environment opt-in, secret-free API status, sanitized Ollama/cloud errors, bounded retry for cloud 429/transient 5xx before streamed output, explicit cancel endpoint, first-token timing and output-character usage history, additive SQLite migration 5→6.
- **Local tests:** 74 passed, 1 Windows-specific credential-vault test skipped on Linux; real localhost HTTP smoke 14/14, nine TS/TSX source files passed syntax checks, **not** a production UI build.
- **Unverified:** new Windows binary, installer, live Ollama/OpenAI provider, OS vault, real audio devices, diarization and isolated Docker execution until CI or hardware testing runs.
- **Requirements:** 144 tracked items (130 previous IDs plus 14 original-master gaps), with conservative statuses in [Feature completion matrix](docs/FEATURE_COMPLETION_MATRIX.md).
- **Privacy:** Windows credential write/read/delete runs under the user's OS account; keys are not stored in SQLite or exports. On Linux there is no in-app secure credential vault, so use a development environment variable only. Cloud is never silently selected. Disable cloud via Settings even when legacy environment opt-in exists.

For this development branch, run [Windows v0.6 validation](.github/workflows/windows-v06-validation.yml) on a real Windows CI runner after publishing the branch. It performs the real OS credential-vault regression in a temporary CI account and checks that an NSIS installer is produced. **This workflow is not installation, upgrade, hardware, or security certification.**

## Historical v0.4/v0.5 Windows release evidence (not v0.6)

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

## Historical v0.4 preview installer (not v0.6)

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

React/Tauri UI → scoped Rust command / authenticated local worker API → Python worker → SQLite and user-chosen providers. The standalone browser companion uses local loopback access and should not be exposed beyond a trusted machine. Cloud inference is explicitly disabled by default. API keys are never included in the source archive or Windows binaries. OS credential vault code is integrated in v0.6; Windows acceptance testing and signed update distribution remain pending.

See [architecture](docs/ARCHITECTURE.md), [security notes](docs/SECURITY.md), [troubleshooting](docs/TROUBLESHOOTING.md), [v0.4 release report](docs/V04_RELEASE_GATE.md) and [test results](docs/V04_TEST_REPORT.json). Project source is MIT licensed. This application must not be used to bypass proctoring or recording restrictions.


## v0.5.0 engineering changes

- Assessment API and desktop controls now accept single-choice, multiple-choice and numerical questions, with numerical tolerance, negative marking and section scores.
- Session-bound transcript **text** can optionally be saved, exported, recovered and deleted; no raw audio is retained. Live audio still does not provide validated speaker diarization.
- Local Python regression suite and source syntax checks are documented in `docs/TESTING_AND_ACCEPTANCE.md`.
- **Release gate:** this v0.5.0 source has not yet been compiled or acceptance-tested as a Windows installer. The earlier v0.4.0 installer is not a v0.5.0 installer. See `docs/FEATURE_COMPLETION_MATRIX.md`.

## v0.6 cloud key setup (Windows)

Launch the Tauri desktop app, open **Settings → Cloud AI**, save an OpenAI key into **Windows Credential Manager**, then click **Enable cloud**. In Live Practice, explicitly select Cloud as the provider. A local Ollama model remains the default. Keys are masked in Settings and never returned by an API, copied into export data, or included in distributed source.

If a key already exists in the `OPENAI_API_KEY` environment variable, it remains supported for developer compatibility, but cannot be deleted through the in-app Windows vault control; remove it manually from the development environment. The native `STUDIO_WORKER_TOKEN` protects its worker API; never expose the worker externally.
