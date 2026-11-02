# v0.6.0 engineering changes — not a production acceptance sign-off

## Delivered source changes

1. Windows Credential Manager generic credential API with scoped key ID and masked status; API does not serialize credentials.
2. User-controlled explicit cloud consent persisted separately from credentials, overriding older environment defaults.
3. Sanitized model-provider errors and retry of transient cloud HTTP 429/5xx responses **before** any tokens are emitted (maximum three attempts). No silent cloud fallback.
4. First-token latency in streamed completion events and per-session response metadata (`ai_usage` table); output characters only, **not** actual API-billed token counts.
5. SQLite migration v5→v6, foreign-key delete cascade for usage history, existing session and transcript preservation tested.
6. Desktop Settings cloud consent, password-key entry and credential deletion controls; explicit cancel endpoint and UI cancellation linkage.
7. v0.6 Windows CI with real OS vault test and installer existence gate, plus refreshed requirement-by-requirement gap audit.

## Tested in current Linux container

- 74 Python tests passed; 1 Windows Credential Manager integration test skipped.
- 14/14 real local HTTP smoke checks passed, using an authenticated localhost Uvicorn process and fresh temporary SQLite database.
- Python compileall and TypeScript/TSX **syntax transpilation** passed. Not equivalent to full TypeScript type checking or React build.
- Cloud adapter tests use deterministic `httpx.MockTransport` HTTP fixtures; no real provider or billing verified.
- Real Docker execution, audio devices and target Windows hardware were unavailable.

## Release gates still open

Full Windows production build, packaged-worker launch, actual installer/upgrade/uninstall verification for v0.6, real local/cloud AI with opted-in credentials, multi-speaker diarization, Docker sandbox e2e tests, real Windows audio devices, signed distribution, RAM/latency on target laptop.

Historical v0.5 Windows installers and portable distributions remain v0.5 and must never be renamed to v0.6.
