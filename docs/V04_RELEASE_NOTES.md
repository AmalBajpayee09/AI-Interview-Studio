# AI Interview Studio v0.4.0 — incremental source preview

Preserves the existing v0.3 codebase and its database migrations. Includes:

- Manual pause/resume for opt-in audio capture, bounded queues, and approximate utterance start/end timestamps. Speaker attribution remains unknown unless verified.
- Bounded sample/custom test suite runner endpoint with one independent Docker container per test, and refusal when Docker capability is unavailable.
- Bounded output-size monitoring for containerized execution to prevent malicious programs from exhausting host memory; cleanup via verified Docker container ID.
- Persistent local coding drafts per programming language, with save and restore in the desktop UI.
- New v0.4 Python regression tests and actual Linux HTTP performance data.
- A PowerShell source-import helper to create a GitHub import branch and generate a real frontend lockfile in a networked Windows environment.

Critical unverified capabilities include the React production build, Rust/Tauri compilation, Windows packaging, live device audio, real provider inference and real Docker runs. They are not claimed as completed.
