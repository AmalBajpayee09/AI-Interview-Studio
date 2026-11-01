# Windows setup for beginners (Windows 10/11)

**What you will have:** (a) a working browser-based companion with no Node/Rust requirement; (b) a Windows desktop Tauri development app if the native toolchain succeeds. A signed/verified installer is **not** included in the source ZIP. Work in your own mock interviews only.

## 1. Check the PC

Open **Start → type PowerShell → Windows PowerShell → Open**. Paste one command at a time:

```powershell
[Environment]::OSVersion.Version
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
Get-PSDrive C | Select-Object Free,Used
```

Target baseline: Windows 10/11, ~16GB RAM, i5 11th gen. For development use at least several GB of spare SSD space; local models add several GB more.

## 2. Install mandatory tools

For the browser companion: **Python 3.11 (64-bit)** from https://www.python.org/downloads/. Tick “Add Python to PATH” if offered. Python 3.11 is chosen as a broad compatibility target for STT libraries; test newer versions before upgrading.

For the **native Windows desktop** additionally install:

1. **Node.js LTS** from https://nodejs.org/en/download.
2. **Git** (optional for this extracted ZIP) https://git-scm.com/download/win.
3. **Visual Studio Build Tools 2022** from https://visualstudio.microsoft.com/visual-cpp-build-tools/, select **Desktop development with C++** and the Windows SDK.
4. **Rust** from https://rustup.rs or `winget install --id Rustlang.Rustup`; use `stable-x86_64-pc-windows-msvc`.
5. **Microsoft WebView2** Evergreen Runtime from https://developer.microsoft.com/en-us/microsoft-edge/webview2/. Often preinstalled.

Close and reopen PowerShell. Check:

```powershell
py -3.11 --version
node --version
npm --version
rustc --version
cargo --version
git --version
```

If you only want the companion, Node/Rust/C++ Build Tools/WebView2 are **not needed**.

## 3. Extract the source ZIP

Download `AI-Interview-Studio-Source-v0.2.0.zip` and open File Explorer → Downloads. Right-click ZIP → **Extract All**, choose `C:\Projects`. Open the `AI-Interview-Studio` folder (the one containing `.env.example` and `scripts`). In its File Explorer address bar, enter `powershell` and press Enter. Verify:

```powershell
Get-Location
Get-ChildItem .\scripts
```

Optional: open this folder in Visual Studio Code with `code .` (install VS Code if desired).

## 4. Install the Python worker

In the project-root PowerShell window:

```powershell
py -3.11 -m venv .\services\ai_worker\.venv
.\services\ai_worker\.venv\Scripts\python.exe -m pip install --upgrade pip
.\services\ai_worker\.venv\Scripts\python.exe -m pip install -r .\services\ai_worker\requirements.txt
Copy-Item .\.env.example .\.env
```

These commands do not require activating a virtual environment. If PowerShell blocks an activation script, continue using the explicit `\.venv\Scripts\python.exe` path instead of changing machine-wide execution policy.

## 5. Run the tested companion first

```powershell
.\scripts\run-browser.ps1
```

Open http://127.0.0.1:8765 in Chrome or Edge if it didn't open automatically. Choose Timed assessments; start the starter quiz. The API health route is http://127.0.0.1:8765/api/health. Leave that PowerShell window open while practicing.

## 6. Install native UI dependencies

Open **a new PowerShell window** inside the root folder. With internet access:

```powershell
cd .\apps\desktop
npm install
cd ..\..
```

`npm install` is intentional: no npm lockfile is shipped because package-registry access was unavailable during artifact creation. After installing, npm generates a lockfile on your machine. Resolve install errors before proceeding.

## 7. Configure local AI (optional but needed for answers)

Install Ollama from https://ollama.com/download/windows. Open PowerShell:

```powershell
ollama --version
ollama list
ollama pull qwen2.5:3b
ollama list
```

Ollama normally starts a local service on `127.0.0.1:11434`. If it doesn't, run `ollama serve` in another terminal. The sample Qwen 3B model is a **starting choice**, not a quality guarantee; its memory, speed and multilingual quality must be measured on your i5 laptop. Open `.env` in Notepad (`notepad .env`) and set `OLLAMA_MODEL=qwen2.5:3b`. For slower CPUs try a smaller compatible model, but verify what is installed. Model weights are never silently downloaded by the app.

## 8. Configure cloud AI (optional and off by default)

Get your own API key from the provider and set these lines **locally** in `.env`:

```ini
ALLOW_CLOUD=true
OPENAI_API_KEY=replace_with_your_private_key
CLOUD_MODEL=gpt-4.1-mini
```

Never put keys in source control or share `.env`. Selecting **Cloud** from the UI sends the current question and relevant session/document context to the configured provider. Turn off with `ALLOW_CLOUD=false` and restart the worker. Model access, rate limits and billing depend on your account. The tested offline quiz requires no cloud key.

## 9. Run the native desktop in development

Close the companion to free port 8765. In a project-root PowerShell window run:

```powershell
.\scripts\dev.ps1
```

This launches the Python worker and starts Tauri/React. The desktop UI is served at port 1420 in development, and talks to the worker on loopback. To debug separately, use two PowerShell terminals:

Terminal 1:

```powershell
. .\scripts\load-env.ps1 -Path "$PWD\.env"
cd .\services\ai_worker
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Terminal 2 from the project root:

```powershell
cd .\apps\desktop
npm run tauri dev
```

## 10. Run tests

```powershell
cd .\services\ai_worker
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe bench.py
cd ..\..\apps\desktop
npm run build
cd .\src-tauri
cargo test
```

Or after setup run `.\scripts\test.ps1` in the project root. Expected success is exit code `0` and no error output. Any test that cannot run is **not passed**.

## 11. Build a Windows installer (unverified path)

From project root:

```powershell
.\scripts\build.ps1
```

It installs PyInstaller into the worker venv, builds a standalone `ai-studio-worker.exe`, then builds Tauri with an NSIS installer resource. Check `apps\desktop\src-tauri\target\release\bundle\nsis` for a `.exe` installer only if the build reports success. You may need Windows SDK/C++ Build Tools and Rust MSVC installed. There is no code signing configured; if Windows warns about an unsigned build, verify what you built before continuing.

## 12. Verify the packaged app

After any successful Windows build: (a) install in a normal user environment; (b) launch and check the worker online; (c) start an offline quiz; (d) verify a saved session; (e) test Ollama and then cloud only if configured; (f) test a PDF/document upload; (g) test microphone permissions and optional STT; (h) test the user-visible compact window; (i) restart and recheck history; (j) run `scripts/diagnose.ps1` for any failure. **This list has not been executed on a Windows host here.**

For a **packaged** worker, place optional local `.env` configuration in `%USERPROFILE%\.ai-interview-studio\.env` (create the folder if needed). Do not share this file. Alternatively set Windows user environment variables. Restart the app after changes.

## New in source preview v0.2.0

The starter dashboard now includes a SQL practice lab (read-only fixture). In the native UI, assessment answers and review marks autosave to SQLite and restore on reopening the same quiz. The companion autosaves selected MCQ answers as well. The Settings screen provides SQLite backup export; restore requires stopping the worker and using `py -3.11 scripts/restore-database.py "C:\path\to\ai-interview-studio-backup.sqlite3"`. See `docs/USER_GUIDE.md`.

The user-facing setup instructions still require Python manually because a complete Windows installer could not be built in the current Linux environment. This source archive is not a prebuilt installer.
