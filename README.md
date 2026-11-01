# AI Interview Studio

AI-powered interview and assessment desktop application (Tauri 2 + Rust + React/TypeScript + Python/SQLite).

## Current status — v0.4.0 source preview

**The full application source is not yet committed to this GitHub repository.** The complete updated source is available as `AI-Interview-Studio-Source-v0.4.0.zip` in the ChatGPT conversation. This public repository currently contains repository-init files, an import guide, and a working Windows CI gate.

[Windows build workflow](.github/workflows/windows-release.yml) — [actual Windows CI run #41346727566](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41346727566) failed at the expected complete-source check: `apps/desktop/package.json` is absent. **No Windows installer has been built.**

## Import source

1. Download and extract the v0.4.0 source ZIP from the project conversation.
2. On a Windows PC with Git, Node/npm, and a network connection, open PowerShell in the extracted `AI-Interview-Studio` folder.
3. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\publish-github.ps1`.
4. Review the new `import/v0.4.0` branch and open a pull request to `main`. The Windows build workflow will run automatically and fail if actual compilation or bundling fails.

See [IMPORT_SOURCE.md](IMPORT_SOURCE.md) for a safety checklist and expected release artifacts.

**This README does not claim a verified installer, compiled native application, real audio-device test, real Docker execution, or an actual model-inference benchmark.**
