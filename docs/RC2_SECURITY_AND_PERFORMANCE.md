# RC2 security, diagnostics, resource and deployment status

**Worker:** Tauri launches a loopback FastAPI sidecar with a per-launch random token. An authenticated health check gates Rust-to-renderer connection; structured lifecycle and readiness markers exclude the secret. This does not protect against malware executing as the same Windows user, compromised renderer/XSS, or external software reading its own credentials. Standalone dev worker may run without STUDIO_WORKER_TOKEN: never bind to a public interface.

**Cloud keys:** Windows Credential Manager abstraction is present; legacy environment-variable key fallback remains and must be reviewed. Cloud inference is opt-in. Redact keys, auth headers, transcripts, source code and resumes from diagnostics.

**Coding:** real Docker isolation tested previously on Linux CI, but Windows Docker Desktop is unverified. No unrestricted host-process fallback is permitted. The Docker daemon and mounted workspace remain a trust boundary.

**Data:** SQLite stores sensitive session/resume content without application-layer encryption. Backups and preserved user data after uninstall need clear user controls, filesystem permissions and data minimization. Receipt and draft migration v7 maintains old data.

**Audio:** no covert capture or default raw-audio storage; real consented Windows microphone/loopback acceptance and multi-speaker quality measures unavailable.

**Installer:** NSIS signing, Windows Defender reputation, update signing and complete rollback are NOT verified. The Rust dependency lockfile is not committed: the Windows build artifact includes the resolved Cargo.lock as evidence, but reproducibility remains a release-quality gap.

**Performance:** only prior Linux HTTP/worker measurements exist, not target Windows laptop model latency. RC2 Windows CI will record installed startup and restart timings if the test passes, but a hosted Windows runner is not a low-resource target laptop. CPU/RAM, audio and real-provider TTFT/p50/p95 require measured hardware-specific runs.

Production security certification: NOT CONDUCTED. Release approval: NOT GRANTED.
