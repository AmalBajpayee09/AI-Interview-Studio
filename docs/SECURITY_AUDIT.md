# Security audit — v0.5.0

## Current protection (source-reviewed; tests where noted)

- Tauri Rust worker starts on loopback with a random per-launch token and dynamic port. API token enforcement + origin guard tested in Python (`test_v03.py::test_worker_token_required`). This does not prove resistance against malware running under the same Windows account.
- SQL practice runs only against disposable in-memory SQLite sample data. The SQLite authorizer, query-only setting, execution deadline, result limits and blocked SQL functions are tested (`test_upgrade.py`). Not an OS-level sandbox.
- Candidate programs are **never** executed as host code by the API. The Docker adapter requires a responding engine and an installed image, with caps, read-only source mount, no network, dropped capabilities, nonroot UID and container cleanup. The real container isolation boundary is **not verified**; absent Docker returns HTTP 503.
- File uploads enforce size/type limits, support user-triggered OCR, and do not execute uploaded code. More malformed/hostile PDF and DOCX fuzz testing is needed.
- Speech capture requires an explicit start action; received utterances are not persisted as raw audio. Text transcription persistence is an **unchecked opt-in** by default and requires a selected session. Session records are deleted with cascading transcript cleanup. SQL migration 005 is incremental.
- Only the user-selected cloud provider receives task data; cloud is disabled by default. Resume/transcript snippets are now passed as *user-level reference data*, not system commands; full prompt-injection resilience is **not guaranteed**.

## Unresolved risks / blockers

1. **HIGH — production credential storage:** cloud API key is currently loaded from `.env` / environment variables, not Windows Credential Manager. Configuration file access permissions and secure migration need validation.
2. **HIGH — Docker isolation validation:** Windows Docker security configuration, mount paths with spaces, process-tree termination, output flooding and container cleanup must be exercised using genuine containers.
3. **HIGH — hardware transparency:** no verified multipeaker diarization; source IDs must never be represented as speaker identity. No permission bypass or stealth/proctoring modifications.
4. **MEDIUM — local HTTP surface:** authenticated desktop mode is better, but standalone browser companion can start without token; bind only to 127.0.0.1 and do not expose to untrusted local processes.
5. **MEDIUM — dependency audit:** no current npm/Rust/Python vulnerability scan due unavailable build dependencies; run scanner in Windows CI.
6. **MEDIUM — native crash/restart:** worker crash recovery and orphan-process cleanup under abnormal Windows termination require testing.

## Pre-release security gate

Do not ship v0.5 as production until secure key storage, real Docker tests, v0.5 Windows package checks and confidentiality tests pass. Avoid storing raw recordings by default. Require explicit user action before capturing microphone/system audio or sending private context to cloud.
