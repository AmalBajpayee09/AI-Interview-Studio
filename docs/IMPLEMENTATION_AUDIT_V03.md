# v0.3.0 inherited-code audit and changes

Source: uploaded `AI-Interview-Studio-Source-v0.2.0.zip`, extracted without executing archive contents. All v0.2 SQLite tables and endpoints remain intact. The original requirements PDF and the earlier completion add-on remain in `docs/`.

| Area | v0.2 blocker / cause | v0.3 remedy and evidence | Remaining limit |
|---|---|---|---|
| React build | No `package-lock.json`, no `node_modules`, offline npm registry; original check transpiled syntax only | Frontend project retained; TypeScript syntax transpiled on 9 files, CI now generates a lockfile on Windows and runs **npm ci** and `npm run build` | Actual production bundle not generated here; CI-generated lockfile must be committed |
| Rust/Tauri | No Rust/Cargo installed, no rust crates locally, and DNS blocks toolchain downloads | Native worker connection now owns its token + port, and resource path is checked; Windows CI runs `cargo check` and `cargo test` | Native compilation not run; Windows must confirm resource setup |
| Installer | No Windows build environment and no Windows CI execution credentials | Windows CI builds Python PyInstaller worker, React assets, and Tauri NSIS, checks installer hash, uploads evidence | No real `.exe`; no clean Windows installer test |
| Worker authentication | Fixed port 8765 and no per-request auth in packaged build | Packaged Rust shell chooses ephemeral loopback port and random per-launch token; frontend sends token; 401 without token | Standalone browser/dev server intentionally runs unauthenticated (loopback only) |
| Isolated code execution | Python AST syntax check, no runner | New optional Docker command runner: explicit image prerequisites, no network, read-only root, nonroot user, reduced caps, time/memory/pids limits, result comparison; endpoint and UI; unit security tests | Docker not installed here; no actual container execution or Windows sandbox validation |
| Dual-source transcription | Uploaded audio and manual browser recording only | Experimental opt-in local SoundCard device capture + short bounded chunks + RMS gate + faster-whisper final transcript events + source IDs; UI controls | No true diarization, partial transcript decoding, or real Windows-device tests; speaker remains unknown |
| AI generation latency | No configured Ollama or cloud credentials | Retained genuine HTTP adapters and mocked stream tests | Cannot benchmark actual model latency |
| Audio latency | No audio hardware and optional STT packages not installed | Added event timestamps and per-utterance transcription latency measurement when enabled | No measured live-device latency |
| SQL/data | v0.2 SQLite read-only engine and drafts tested | Preserved existing schema and migrations; no destructive updates | No Windows clean-install validation |

## Environment inspection

Linux x86_64, Python 3.13.5, Node.js v22.16.0, npm 10.9.2; TypeScript v5.8.3 globally available. Rust/Cargo not installed. npm registry lookup fails DNS, and `npm install --package-lock-only --offline` failed `ENOTCACHED` for `@tauri-apps/api`. Windows build tools/Wine absent. No explicit GitHub repo or authenticated CI runner was supplied.

## Evidence and limitations

- `python -m pytest services/ai_worker/tests -q` with `PYTHONPATH=services/ai_worker`: 41 tests passed (Linux, 2026-11-02 UTC-relative project date).
- Live HTTP smoke: 6/6 checks passed, including unauthorized 401 and authorized 200, source status and capabilities.
- JSON/Tauri configuration and Windows CI YAML parse.
- 9 TS/TSX source files: syntactic transpilation successful (NOT a full production build or typecheck).
- Installer, end-user Windows tests, Docker isolation, true audio diarization, real provider calls: **not executed**.
