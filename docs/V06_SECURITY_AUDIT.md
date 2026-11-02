# v0.6 security audit — bounded, evidence-based

| Control | Current result | Remaining risk |
|---|---|---|
| Windows OS credential store | `CredWriteW`/`CredReadW`/`CredDeleteW` implemented in worker | Real API validation requires Windows runner; user-account permissions and PyInstaller behavior unverified locally |
| No plaintext export/logs | API returns masked status only; Python test ensures sample key absent from SQLite export | Developer environment variable remains allowed for backward compatibility; process environment can reveal it |
| Explicit cloud consent | SQLite Boolean override and tested disable even with prior env allow | No real cloud request performed; provider's external retention policy is outside our control |
| Cloud network error sanitation | HTTP 401/429 fixtures check error does not reveal body; transient retry bounded | Provider usage tokens and invoices not available, real rate limiting unverified |
| Local worker authentication | Historical tested token and dynamic port | Local privileged processes can inspect same-user child environment; standalone dev browser server has no token by default |
| Code sandbox | Docker isolated-run adapter refuses when unavailable | No actual Docker runtime or adversarial Windows sandbox test in this cycle |
| Audio permissions/consent | Existing explicit start/stop; no raw audio saved by default | No validated multi-speaker diarization, device disconnection or WASAPI loopback on Windows |
| Database migrations/backup | v5→v6 additive migration tested with transcripts and session; SQLite online backup present | Automatic disaster recovery from corrupt DB and fresh-to-upgrade Windows installer test remain unverified |
| Third-party dependencies | Pinned Python requirements and npm lockfile preserved | No automated package vulnerability or signed-binary supply-chain scan |

Do not expose worker HTTP to the network. Use a trusted Windows account. Never bundle user secrets with GitHub source or CI artifacts. Existing tests use synthetic `sk-test...` fixtures, not real keys.
