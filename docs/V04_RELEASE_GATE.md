# AI Interview Studio v0.4.0 — evidence-backed release gate

**Status: Installable Windows preview. Not a fully validated production release.**

All 102 transferred source files were checked against their GitHub Git-blob hashes before the import PR was merged into `main`. Main now contains the complete source, TypeScript/Rust desktop project, tests, scripts, and a genuine npm lockfile.

| Verification | Status | Evidence / limitation |
| --- | --- | --- |
| Complete GitHub source on `main` | PASS | PR #1 merged, all 102 transferred source files byte-verified |
| Dependency lockfile | PASS | Generated on Windows CI, committed and independently downloaded |
| Windows React + TypeScript production build | PASS | Windows CI 41347613395 and 41347725338 |
| Python backend on Windows | PASS | 51 tests, 0 failed/skipped in CI artifact |
| Rust check and test on Windows | PASS | Windows CI 41347725338 |
| Python worker packaging | PASS | Real PyInstaller/Tauri release build, Windows CI 41347725338 |
| NSIS Windows installer | PASS | Real executable 123,684,738 bytes, SHA-256 verified |
| Windows installation and desktop/worker launch smoke | PASS | Windows CI 41349033077; silent installation, process/worker check, uninstall attempt |
| Portable archive creation and startup | PASS | Windows CI 41349033077 created package; 41349336117 launched it with worker after extraction. Locally cleaned version omits uninstaller |
| Full clean-machine user install/upgrade/uninstall acceptance | PARTIAL | CI silent install and uninstall attempted; upgrade, GUI workflows, and full cleanup not exercised |
| Real continuous two-speaker diarization | BLOCKED | Device/fixture accuracy tests not performed; current module uses explicit unknown fallback |
| Real Windows microphone/system loopback | BLOCKED | Hardware permissions/capture not tested |
| Genuine Docker code execution on Windows | BLOCKED | No Docker runtime configured in this run; runner unit/mocked tests only |
| Real local Ollama and cloud inference | BLOCKED | No connected live model or configured test credentials |
| Resource governor/target Intel i5 laptop performance | PARTIAL | Linux HTTP/worker benchmarks only; target laptop not tested |
| Signed release / supported automatic updates | NOT STARTED | Installer is unsigned; hash verified only |

**Windows installer SHA-256:** `bfcdeb9d232e4bd02119bdc5b39f0913f1421607334ee07a65116a6eacbdc8f9`

**Portable ZIP SHA-256 (locally cleaned):** `d91f4c51b1d8b8261eb30d2e8a60ec36e9a193dc10a23108fc3d3d3b2e361e33`

- [Windows native build](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41347725338)
- [Installer smoke](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41349033077)
- [Portable launch smoke](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41349336117)
- [Source import PR #1](https://github.com/AmalBajpayee09/AI-Interview-Studio/pull/1)

**Do not confuse** actual installer build and process startup success with proof that live AI, audio, third-party meeting integrations or secure exam-browser overlays work. Those require further evidence. No model download weights or real API credentials are included.