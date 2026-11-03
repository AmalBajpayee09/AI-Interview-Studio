# Windows RC1 installation and acceptance protocol

On a clean Windows x64 machine/VM, obtain the installer from the **exact final-commit** GitHub Actions run, verify SHA-256, and record OS build, CPU/RAM/GPU, WebView2, Defender and installed paths. Do not use an older installer.

1. Install to a path with spaces; launch the actual desktop. Confirm authenticated Tauri→worker readiness, SQLite v7 initialization, first-launch logs and absence of tokens/credentials.
2. Create a timed assessment in the desktop UI with duration 2m, penalty 0.5 and cutoff 75%. Answer, autosave, close app, relaunch, recover answers/start/deadline, submit; retry and confirm only one attempt. Repeat with time expired and verify timely saved answers only.
3. Kill worker mid-request; verify bounded recovery, visible errors and no orphan worker at shutdown.
4. Test genuine Ollama model discovery, stream, cancellation, contextual follow-up and persistence, with Ollama/model/version recorded. Cloud test requires user-approved credential and consent.
5. Test Docker Desktop Linux container isolation with four language images; validate network/file isolation, output/memory limits, timeout and cleanup.
6. With explicit consent, test actual microphone/loopback selection, speech transcription timestamps, disconnection and qualified speaker attribution. No secret recording.
7. Upgrade from the previous supported version with persistent user data; uninstall and reinstall; record which data remains.

Classify each stage PASS, FAIL or BLOCKED with actual steps, logs, observed result, expected result, environment and checksums. A passing cargo check is not end-to-end Windows acceptance.
