# AI Interview Studio v0.4.0 — Windows installable preview

## Build and release milestones

This incremental update preserves v0.3.0 functionality, adds coding practice and audio controls, and produces the **first real compiled and smoke-tested Windows installer**.

- Source imported to `AmalBajpayee09/AI-Interview-Studio`, PR #1 merged to `main`.
- Real npm lockfile generated and committed by the Windows CI bootstrap run.
- GitHub Windows native build succeeded: 51 Python tests, React/TS production build, Rust checks/tests, PyInstaller worker bundle and Tauri NSIS installer.
- Installer file `AI-Interview-Studio-Setup-v0.4.0.exe` is 123,684,738 bytes; SHA-256 `bfcdeb9d232e4bd02119bdc5b39f0913f1421607334ee07a65116a6eacbdc8f9`.
- CI silent install plus desktop/worker startup smoke passed; CI silent uninstall step succeeded.
- Portable Windows package created; CI validated a standalone portable desktop process and worker launch. Cleaned local archive contains the two executables only.

## New modules

- Manual pause/resume for opt-in experimental audio capture, bounded buffering and approximate utterance timestamps. No guaranteed diarization.
- Multi-test-case runner for Docker-isolated coding practice with disabled/no-Docker behavior, resource and output limits, cleanup, and per-language draft recovery.
- Worker auth and local privacy features preserved.

## Known limitations

This is a working **installable preview**, **not** a fully validated production release. No real two-speaker Windows audio testing, high-quality diarization validation, genuine Ollama/cloud inference, target Intel i5 laptop benchmarking, or real Docker container execution was done. No signed binary or end-to-end upgrade/GUI workflow verification. More information: [release gate](V04_RELEASE_GATE.md).

### Build evidence

- [Native Windows build](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41347725338)
- [Installer smoke](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41349033077)
- [Portable smoke](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41349336117)