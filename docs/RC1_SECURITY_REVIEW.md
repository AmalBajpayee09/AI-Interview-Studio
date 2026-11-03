# RC1 security checkpoint (not a full security signoff)

- RC1 strict timed scoring uses server-held clock and grading policy and SQLite transactionally stored receipts. Old direct-submit quizzes remain **legacy self-practice**, not remotely proctored exams. The local machine owner can alter the host clock/database; secure testing requires an external trusted service and threat model.
- Worker per-launch auth and origin restrictions existed before this milestone. The real-worker subprocess smoke confirms 401 for missing/bad token and no token in lifecycle logs.
- Backend strips answer keys from candidate-facing assessment listings; keys appear in results after submission. This is NOT high-stakes exam secrecy where the candidate controls the local database.
- Inherited Windows secure credential adapter, cloud opt-in, Docker Linux VM and audio privacy require separate production security acceptance.
- No raw audio, API key, token or private resume is embedded in this RC1 source branch. Do not commit SQLite user data or logs.
- Remaining review: Windows file ACLs, Tauri capability/IPC authorization, dependency vulnerability scan, upload file parsers, container daemon access, CSRF/origin and token lifecycle, retention/deletion, installer signing and independent threat-model review.

**Release gate: unresolved.**
