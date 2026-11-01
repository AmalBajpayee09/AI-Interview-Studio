# Security and privacy review (preview)

- Scope: explicit user-authorized mock interview and learning. The software is not meant to circumvent exam browser restrictions, monitoring, application deny-lists, endpoint security or proctoring. No undetectable overlay, process hiding or click-through evasion.
- Current worker binds only to `127.0.0.1`. `Host` and `Origin` checks mitigate some browser cross-origin traffic, but the loopback API does **not authenticate local native processes**. This is insufficient for a high-assurance shared-computer threat model. Do not expose the port to the internet or untrusted network interfaces.
- Keys may be in a local plaintext `.env`; never log or upload credentials. Database stores session/document content locally but **without encryption at rest**. Cloud is disabled by default.
- Do not execute generated code. AST parse detects only Python syntax and is not an execution sandbox. No code runner is provided until genuine OS-level sandboxing is established.
- Direct PDF and image parsing is in process, and potentially malformed uploads can hit third-party parsers. There are file size/page/pixel limits but no specialized parser isolation. Only import files you trust.
- During transcription, audio is stored in a temporary file and deleted after processing. No raw audio persistence is enabled. Recording occurs only after microphone access is granted.
- User-triggered JSON export includes full documents and session turns, so protect exported files. Cloud provider request contains the question and recent user-provided context. No opaque automatic cloud fallback. `ALLOW_CLOUD=false` is the privacy-preserving default.
- Third-party model outputs can hallucinate. Response status is unverified unless separately verified by a deterministic tool. No hidden-test claims.
- Safe Exam Browser source archive was inspected as reference only, not patched. Original source carries MPL-2.0 license. See `SEB_MOCK_TESTING.md`.
- The original user specification asks for a Windows test harness and capture-compatible overlay; current on-top window is visible and standard, not capture-protected. Compatibility and accessibility testing are pending.

Release blockers: authenticated IPC, OS key store, signed updater/installer, dependency audits, native Windows testing, and security review for end-user deployments.
