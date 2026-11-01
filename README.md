# AI Interview Studio

Windows desktop interview-practice application, developed with Tauri 2, Rust, React/TypeScript, Python and SQLite.

**Release status: source preview v0.3.0 — not yet a verified Windows installer.**

This repository is being initialized from the verified `AI-Interview-Studio-Source-v0.3.0.zip` archive shared in the project conversation. The archive contains the application source, Windows packaging workflow, tests and documentation.

**Import remains required before building:** the full source tree (folders `apps/`, `services/`, `scripts/`, `docs/`, `shared/`, and the hidden `.github/` directory) must be committed here. GitHub Actions must never be considered successful until the workflow compiles the native app and produces an actual installer artifact.

After the source is imported, run `.\scripts\build.ps1` on Windows or the `.github/workflows/windows-release.yml` workflow using Actions.

This README is an initialization marker, not a claim that the source has already been uploaded.