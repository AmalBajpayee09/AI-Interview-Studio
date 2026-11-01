# Windows native release — exact reproducible continuation

There is **no Windows installer** in the source ZIP. The CI workflow is present but has **not been executed**. Source ZIP ≠ Windows `.exe`.

## First Windows CI run

1. Push the included project files to an authorized GitHub repository, including `.github/workflows/windows-release.yml` (do not push `.env`, personal sessions, or API keys).
2. Go to **Actions > Windows native build and installer > Run workflow**. A repo with GitHub Actions enabled is required; ChatGPT cannot run workflows without connected, authorized repository access.
3. The runner installs Python 3.11, Node 22, Rust stable and uses Windows build tools. It runs Python tests; generates a dependency lockfile **because the uploaded v0.2 archive omitted one**; uses `npm ci`; runs `npm run build`, `cargo check`, `cargo test`; packages the worker with PyInstaller; runs Tauri NSIS bundling; checks installer existence/hash; uploads artifacts.
4. Download the `windows-build-artifacts-and-logs` artifact from the workflow run. Commit the generated `apps/desktop/package-lock.json` to the repository for future reproducibility.
5. **Do not distribute** until real Windows clean-machine tests pass: install, first launch, bundled worker startup, authenticated connection, opening the compact overlay, restart, upgrade, uninstall, reinstall, local/cloud model errors, microphone loopback permissions, and data retention.

## Manual Windows build (developer machine)

```powershell
.\scripts\setup.ps1
& .\services\ai_worker\.venv\Scripts\python.exe -m pip install -r services\ai_worker\requirements-stt.txt
.\scripts\build.ps1
```

The intended installer path is `apps\desktop\src-tauri\target\release\bundle\nsis\*.exe`, but this path will exist **only after a successful Windows build**. `build.ps1` includes Python worker resource packaging. MSI and portable builds are not yet configured or verified.

## Known blockers today

- Container is Linux, without Rust/Cargo, Windows toolchains or Wine.
- npm and Rust registry resolution is unavailable from the build environment.
- `npm install --package-lock-only --offline` failed `ENOTCACHED`: no lockfile generated here.
- No accessible GitHub repository/workflow run or Windows VM for a real native installer.
- No live Docker, audio device or AI provider was available for end-to-end validation.
