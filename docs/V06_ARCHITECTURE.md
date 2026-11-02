# v0.6 architecture delta

The original Tauri 2/Rust + React/TypeScript + Python FastAPI worker + SQLite design is unchanged.

1. React Settings calls authenticated localhost `/api/cloud/status`, `/api/cloud/credential` and `/api/cloud/consent`. API never returns keys. On Windows only, `app/credentials.py` calls Advapi32 `CredWriteW`, `CredReadW`, `CredDeleteW`, and `CredFree` for a generic per-user Windows Credential Manager target `AIInterviewStudio/OpenAI`.
2. A cloud request is only sent when explicitly selected in the Interview workspace and `cloud_consent` is enabled or its legacy env fallback is true. A saved user setting overrides the legacy environment default. Cloud key is loaded only after explicit selection; local Ollama remains default.
3. Cloud adapter retries HTTP 429/500/502/503/504 or connect exceptions before emitting tokens, max 3 attempts. Errors never include raw provider response bodies or the configured API key. It does not fail over to cloud automatically.
4. The async inference stream records the time to the first emitted token and total duration, then persists a completed answer and AI metadata to SQLite. This metadata is based on real local timestamps, but token billing is not available. Canceled or errored answers do not record a successful usage entry.
5. SQLite v6 adds a session-associated `ai_usage` table and index. All earlier tables, rows and contracts remain in place. Session deletion cascades to usage history.
6. Security scope: loopback worker with per-launch Tauri authentication; standalone developer browser worker is less isolated and should be run only on a trusted workstation. No real Windows firewall/port exposure test has yet been run.

See original `ARCHITECTURE.md`, `SECURITY_AUDIT.md` and `FEATURE_COMPLETION_MATRIX.md` for broader project scope.
