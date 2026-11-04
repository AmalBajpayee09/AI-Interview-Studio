# RC3 recovery checkpoint

**Canonical baseline:** `feature/v1.0-rc2-windows-acceptance` at `dab3130f253fb0620df3a8eb8e8d817692f485a3`.
**Continuation branch:** `feature/v1.0-rc3-production-acceptance`, initially created from that SHA.
**Production `main`:** `b4a9d2b449122a29fa7b874652473648e9384f05`, unchanged.
**Existing review:** Draft Pull Request #10 for RC2, unmerged. No RC3 PR at recovery.

**Canonical source artifact:** `AI-Interview-Studio-v1.0.0-RC2-Canonical-Source.zip`, SHA-256 `cec9abd195902432cdfd7b63451cdff2fc738293cc21c0f583278acfd46eb020`, 204 ZIP entries, CRC passed, ZIP comment embeds RC2 commit SHA. Local source extracted into `/mnt/data/rc3-work/`; it is **not** a Git checkout, so local staged/unstaged changes cannot be inferred from its directory. GitHub branch, remote history, open PRs and workflow statuses were independently checked through the connected GitHub API.

**Architecture:** React/Vite/TypeScript frontend; Tauri 2/Rust authenticated worker supervisor; FastAPI/Python worker; SQLite v7; provider adapters, Docker coding, explicit audio, assessments and resume. Existing working code and history preserved.

**Historic exact-commit RC2 evidence:** [Windows run #41718783390](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41718783390) passed Python 113 / 12 skips, locked React build, Rust checks/tests, NSIS, and 15 installed-app lifecycle/upgrade/recovery phases. No complete WebView assessment, real Ollama generation, Windows Docker Desktop or microphone acceptance was demonstrated.

**Fresh extracted-source Linux baseline:** `PYTHONPATH=services/ai_worker pytest services/ai_worker/tests -q --disable-warnings --maxfail=1` → **112 passed, 13 skipped, 0 failed**. Different environment and different source snapshot from prior reports explain the different count. No real Ollama, Docker, Windows GUI, Cargo or Windows audio devices accessible on this host.

**Confirmed gaps for targeted RC3 work:**
- Assessment result/history is not recoverable through its own dedicated UI read path after restart.
- On a new database, schema initialization can set user_version back from 7 to 6 due to migration ordering.
- Client assessment countdown uses wall-clock `Date.now()`, rather than server-provided deadline and a monotonic display timer.
- Existing Windows CI validates installed native lifecycle and packaged worker API, not assessment interactions inside the installed WebView.
- Actual local/cloud inference, Windows Docker Desktop and real Windows audio remain separate, unverified gates.

Do not treat mocks, source compilation, or a passing API test as installed desktop acceptance. Preserve all existing 157 requirement IDs; append new RC3 IDs separately. Source archives and installers must be generated from the exact tested commit. Production release remains blocked pending live integration and device acceptance.
