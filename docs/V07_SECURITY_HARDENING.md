# v0.7 security integration — GitHub branch (not a production release)

This branch builds on the **newer GitHub v0.6 development branch** rather than overwriting its existing Windows Credential Manager, provider retries, cloud consent, model usage and session features with an older uploaded source snapshot.

## Targeted security fixes
- `POST /api/cloud/credential` now manually validates secret input, because the default FastAPI/Pydantic 422 response echoes rejected input values.
- Malformed Ollama and cloud streaming frames now return generic provider errors instead of crashing on unexpected JSON types.
- New deterministic regression checks for secret redaction and malformed frames.
- A Windows-only credential-manager round-trip test, using an isolated temporary target, runs in Windows CI; it is skipped on other operating systems.
- Manifest versions on this development branch are set to `0.7.0`.

## Verification boundaries

Existing v0.6 GitHub branch contained features not present in the user-uploaded v0.6 source ZIP. The separate archive-based `AI-Interview-Studio-Source-v0.7.0.zip` is a tested integration increment **from the uploaded ZIP**, not an identical checkout of this GitHub development branch. Both branches must be reconciled, CI-tested, and source-archived from an exact commit before a public v0.7 release.

Passing Windows compilation and a test involving OS Credential Manager does not establish real Ollama/cloud inference, real microphone diarization, Docker isolation, end-user installation, upgrade correctness or completed acceptance of the 130 requirements.

Never place cloud keys in GitHub actions logs, SQLite data exports, or committed `.env` files. The legacy process-environment fallback remains supported for existing users and must be migrated carefully.
