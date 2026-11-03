# RC2 Windows build, upgrade and troubleshooting

Source: `feature/v1.0-rc2-windows-acceptance`; preserve production main. Require Windows x64, WebView2 runtime, Python 3.11 for build, Node 22, Rust/Tauri build toolchain, VS C++ build components, and connected network for dependency installation. Locked npm dependencies are committed; Rust Cargo.lock still needs a reproducible committed source.

Build through GitHub Actions workflow `.github/workflows/windows-release.yml` on the exact commit. This packages a PyInstaller worker and a Tauri NSIS setup. Inspect the run conclusion and the `rc2-installer-source-and-windows-acceptance` artifact; do not trust an .exe from a different revision. Compare its SHA-256 with the run summary before installing.

The CI acceptance requires an old `0.9.0` installer from run 41683032273, checksum `6EECCB4E59F3D59069AF44B6565B374F094F370693C24C0704988901B54026B8`. Script checks Unicode path, DB retained session, authenticated worker, crash recovery, relaunch and uninstall, but not real model/audio/Docker.

Diagnostics are in `%LOCALAPPDATA%\\com.interviewstudio.desktop\\logs`: `worker-lifecycle.jsonl`, `worker-readiness.json`, allowlisted diagnostic export, and worker stderr (stderr may contain third-party text; do not share publicly unreviewed). There is no safe reason to include authentication tokens, prompts or credentials.

Troubleshooting: If the worker does not become ready, inspect readiness stage and exit; verify PyInstaller worker exists, WebView2 runtime, install directory permissions and architecture. If a model fails, start Ollama and explicitly select a pulled model; never assume a cloud fallback. If Docker is offline, coding execution should remain disabled. If audio is denied, grant Windows microphone permission or choose a supported capture device.

Manual acceptance remains necessary on the user's target PC for installer upgrade/rollback, audio permissions, provider latency, GPU/CPU resource constraints and full desktop UI workflows.
