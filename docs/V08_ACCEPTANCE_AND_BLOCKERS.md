# v0.8 acceptance and blocker register

**Result vocabulary:** PASS = executed end-to-end with the stated environment. PARTIAL = a narrower unit/API result. BLOCKED = prerequisite absent. The absence of evidence is not a pass.

| Workflow | Preconditions | Steps/evidence in this increment | Result |
|---|---|---|---|
| Fresh worker startup | Python 3.13, Linux | Run packaged source worker, authenticate health over real localhost HTTP, create SQLite session | **PASS** (worker only) |
| Session history and follow-up | TestClient, SQLite, simulated provider | Two SSE turns with prior assistant context, reload and query SQLite | **PASS** (HTTP/SQLite simulated inference only) |
| Live Ollama inference | Ollama installed, running, model pulled | `STUDIO_LIVE_OLLAMA_TEST=1` and `pytest ...test_v08.py -k real_ollama` | **BLOCKED**: no Ollama configured on host |
| Live cloud inference | Windows vault credential, consent, authorized cloud account | `STUDIO_LIVE_CLOUD_TEST=1` and `pytest ...test_v08.py -k real_cloud` | **BLOCKED**: no user credentials/consent supplied |
| SSE cancellation | Python worker and controlled async provider | Cancel session mid-stream; assert no partial assistant turn saved | **PASS** (simulated provider only) |
| Duplicate generation | Worker + session | Second generation in same session returns 409 | **PASS** (API) |
| Persistent assessment | SQLite and practice assessment | Existing mixed-format engine regression tests | **PARTIAL**: desktop UI acceptance not run |
| Isolated code execution | Docker Desktop Linux containers and images | Run Python, JS, Java, C++ and hostile tests in constrained Docker | **BLOCKED**: Docker unavailable here |
| Windows audio & diarization | Windows microphone/loopback devices, consent | Select devices, speak, transcribe, verify speaker attribution | **BLOCKED**: no Windows audio hardware; no reliable validated diarization |
| Credential-vault roundtrip | Windows credential manager | Run OS-specific vault test | **BLOCKED** on Linux; Windows CI separately required |
| Windows Tauri installation | Windows GitHub Actions | NSIS install, start app, verify bundled worker and DB | **PENDING** until exact v0.8 CI run reaches acceptance stage |
| Upgrade and data retention | v0.7 installed data + v0.8 installer | Install over, restart, compare DB and transcript history | **BLOCKED**: previous installer/upgrade matrix unavailable in current environment |
| Portable Windows launch | Built portable Windows bundle | Unpack in fresh directory, start app and worker | **NOT YET VERIFIED** for v0.8 |

## Required next manual steps

On a consented Windows machine, install Docker Desktop Linux containers and explicitly pull the supported images before testing isolated code. Separately install Ollama and a model and enable the opt-in integration test. For cloud, save a test credential through Windows Credential Manager, opt into cloud processing and run the opt-in cloud test. Never place keys in GitHub logs or `.env` committed files. Capture actual device permissions, audio timestamps and speaker attribution accuracy with a recorded two-speaker ground-truth fixture.
