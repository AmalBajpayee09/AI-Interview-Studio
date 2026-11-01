# v0.3 release acceptance matrix — evidence-backed

| Area | Status | Evidence / blocker |
|---|---|---|
| Python API + SQLite compatibility | PASS | 41 automated Python tests; 6 live HTTP smoke checks |
| Code runner fail-closed path | PASS | Tests reject execution without Docker; mock verifies isolation command |
| Secure code execution on Windows | PARTIAL | Docker adapter exists; real Docker image execution not tested |
| Authenticated bundled worker contract | PARTIAL | Python HTTP token tested; Rust build not compiled |
| React source TS syntax | PASS | 9 files parsed/transpiled without syntax diagnostics |
| Full React production build | BLOCKED | Missing lockfile and npm network/cache; no `dist` output |
| Rust/Tauri build | BLOCKED | Rust/Cargo absent, registry inaccessible |
| Windows installer | BLOCKED | No Windows CI access or Windows VM; no `.exe` created |
| Portable distribution | NOT STARTED | Requires verified Windows build |
| Windows CI workflow source | PARTIAL | YAML parsed, not run; first-run lockfile resolution not reproducible until committed |
| Continuous microphone/loopback transcription | PARTIAL | Backend/UI + gate contract tested; device/Whisper test unavailable |
| Speaker diarization | NOT STARTED | Multiple source IDs are not evidence of identity |
| Ollama/cloud live generation | BLOCKED | No local model or user credentials; mocked adapter tests only |
| Resume/MCQ/SQL/historical sessions | PARTIAL | Original features retained and API tests pass; Windows user acceptance pending |
| System design / ML / HR interactive practice | PARTIAL | AI-backed prompts depend on configured untested provider |
| Desktop overlay | PARTIAL | Rust compact-window source exists; Windows not tested |
| Total app memory and real AI latency | BLOCKED | No compiled desktop/model execution |
| Source ZIP integrity | PASS | Archive CRC check and file manifest validated (see `V03_ARCHIVE_MANIFEST.json`) |

**Overall release:** Engineering source preview, **NOT** a completed installable Windows product.
