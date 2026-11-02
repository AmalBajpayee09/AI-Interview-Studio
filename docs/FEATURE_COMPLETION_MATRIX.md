# Feature completion matrix — v0.6.0

**144 requirements audited**: 130 original v0.5 IDs preserved, plus 14 additional master-specification gaps.

Statuses apply only to their documented scope. **No v0.6 feature is declared VERIFIED — END-TO-END without an actual end-to-end test.**

| Status | Count |
|---|---:|
| BLOCKED | 8 |
| IMPLEMENTED — NOT VERIFIED | 1 |
| NOT IMPLEMENTED | 33 |
| PARTIALLY IMPLEMENTED | 82 |
| TESTED — DEFINED CODE-PATH | 20 |

The prior v0.5 installer passed Windows CI smoke checks, but those do **not** verify new v0.6 changes. References to automated tests in baseline entries are historical or code-path only.

The full machine-readable record with previous status, source modules, implementation, missing work, acceptance criteria, automated tests, manual validation, evidence, limitations, and next action is `V06_REQUIREMENTS.json`.

### A-01 — Tauri 2 + Rust + React + TypeScript architecture.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src-tauri/src/lib.rs; apps/desktop/src/App.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_sessions_recovery, test_v05.py::test_existing_schema_v4_upgrades_without_data_loss
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### A-02 — Desktop window lifecycle and native integration.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src-tauri/src/lib.rs; apps/desktop/src/App.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_sessions_recovery, test_v05.py::test_existing_schema_v4_upgrades_without_data_loss
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### A-03 — Floating and compact interface modes.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src-tauri/src/lib.rs; apps/desktop/src/App.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_sessions_recovery, test_v05.py::test_existing_schema_v4_upgrades_without_data_loss
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### A-04 — Global keyboard shortcuts.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `apps/desktop/src-tauri/src/lib.rs; apps/desktop/src/App.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** No global shortcut registration or rebind UI exists.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_sessions_recovery, test_v05.py::test_existing_schema_v4_upgrades_without_data_loss
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### A-05 — Multi-monitor and display-scaling support.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `apps/desktop/src-tauri/src/lib.rs; apps/desktop/src/App.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** No multi-monitor acceptance tests or native monitor picker.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_sessions_recovery, test_v05.py::test_existing_schema_v4_upgrades_without_data_loss
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### A-06 — Window resizing, positioning, minimize and restore.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src-tauri/src/lib.rs; apps/desktop/src/App.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_sessions_recovery, test_v05.py::test_existing_schema_v4_upgrades_without_data_loss
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### A-07 — SQLite persistence and database migrations.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `apps/desktop/src-tauri/src/lib.rs; apps/desktop/src/App.tsx; services/ai_worker/app/db.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_studio.py::test_sessions_recovery, test_v05.py::test_existing_schema_v4_upgrades_without_data_loss
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### A-08 — Application startup, shutdown, crash recovery and logging.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src-tauri/src/lib.rs; apps/desktop/src/App.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_sessions_recovery, test_v05.py::test_existing_schema_v4_upgrades_without_data_loss
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### B-01 — Local AI through Ollama or compatible providers.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/config.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock], test_studio.py::test_cloud_opt_in
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### B-02 — Cloud AI provider integration.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/config.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock], test_studio.py::test_cloud_opt_in
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### B-03 — Provider configuration and API-key management.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/credentials.py; services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** v0.6 Python test_v06.py contract tests (mocked external providers); no real Windows vault or cloud-provider validation.
**Gap:** Real Windows credential-vault test and live-provider end-to-end verification remain; no automatic cloud fallback, and billed token usage is not available.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock], test_studio.py::test_cloud_opt_in
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Validate Windows Credential Manager with a real user account; exercise real cloud provider with user-owned credentials and measure latency/usage.

### B-04 — Model selection and model routing.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/config.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock], test_studio.py::test_cloud_opt_in
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### B-05 — Streaming responses and cancellation.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/config.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock], test_studio.py::test_cloud_opt_in
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### B-06 — Context management and conversation history.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/config.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_studio.py::test_fake_stream_persists [mock], test_studio.py::test_cloud_opt_in
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### B-07 — Retry, timeout, fallback and rate-limit handling.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/credentials.py; services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** v0.6 Python test_v06.py contract tests (mocked external providers); no real Windows vault or cloud-provider validation.
**Gap:** Real Windows credential-vault test and live-provider end-to-end verification remain; no automatic cloud fallback, and billed token usage is not available.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock], test_studio.py::test_cloud_opt_in
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Validate Windows Credential Manager with a real user account; exercise real cloud provider with user-owned credentials and measure latency/usage.

### B-08 — Response latency and token usage tracking.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/credentials.py; services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** v0.6 Python test_v06.py contract tests (mocked external providers); no real Windows vault or cloud-provider validation.
**Gap:** Real Windows credential-vault test and live-provider end-to-end verification remain; no automatic cloud fallback, and billed token usage is not available.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock], test_studio.py::test_cloud_opt_in
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Validate Windows Credential Manager with a real user account; exercise real cloud provider with user-owned credentials and measure latency/usage.

### B-09 — Model availability and health checks.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/config.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock], test_studio.py::test_cloud_opt_in
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### C-01 — Session context memory.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; services/ai_worker/app/logic.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v05.py::test_transcript_context_is_session_scoped [mock provider], test_studio.py::test_sessions_recovery
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### C-02 — Previous questions, candidate responses and code context.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; services/ai_worker/app/logic.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v05.py::test_transcript_context_is_session_scoped [mock provider], test_studio.py::test_sessions_recovery
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### C-03 — Follow-up question understanding.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; services/ai_worker/app/logic.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_transcript_context_is_session_scoped [mock provider], test_studio.py::test_sessions_recovery
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### C-04 — Adaptive answer modes: Hint → Short Answer → Detailed Explanation → Code/Diagram.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; services/ai_worker/app/logic.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_transcript_context_is_session_scoped [mock provider], test_studio.py::test_sessions_recovery
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### C-05 — Verified / Probable / Uncertain confidence indicators.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; services/ai_worker/app/logic.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_transcript_context_is_session_scoped [mock provider], test_studio.py::test_sessions_recovery
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### C-06 — Separation of model confidence from actual tool verification.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; services/ai_worker/app/logic.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_transcript_context_is_session_scoped [mock provider], test_studio.py::test_sessions_recovery
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### C-07 — Smart question segmentation into question, constraints and follow-ups.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; services/ai_worker/app/logic.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_transcript_context_is_session_scoped [mock provider], test_studio.py::test_sessions_recovery
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### C-08 — Context compression and session recovery.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; services/ai_worker/app/logic.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_transcript_context_is_session_scoped [mock provider], test_studio.py::test_sessions_recovery
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### D-01 — Microphone input.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### D-02 — Desktop loopback/system audio input.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### D-03 — Configurable audio sources.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### D-04 — Continuous audio processing.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### D-05 — Speech-to-text transcription.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### D-06 — Speaker diarization.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** No validated acoustic diarization; all source events are speaker unknown.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### D-07 — Candidate-voice filtering where technically reliable.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** Source filtering exists; verified speaker-identity filtering does not.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### D-08 — Configurable transcription and audio indicators.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### D-09 — Audio buffering and latency management.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### D-10 — Device selection and device disconnection recovery.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### D-11 — Explicit microphone permissions and recording controls.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### D-12 — Real Windows audio-device integration tests.
**Status:** BLOCKED · **Previous:** BLOCKED
**Source:** `services/ai_worker/app/audio_live.py; apps/desktop/src/views/LiveAudioControls.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** Requires real consented Windows microphone and loopback devices.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_voice_gate_detects_silence_end, test_v04.py::test_audio_pause_resume_status_and_events [mock state]
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Run on compatible Windows/runner or hardware with required dependencies, record evidence and fix failures.

### E-01 — Python, JavaScript, C++ and Java support.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### E-02 — Code editor with syntax highlighting.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### E-03 — Input/output handling.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### E-04 — Expected-output comparison.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### E-05 — Time and memory limits.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### E-06 — Compilation and runtime error handling.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### E-07 — Multiple test cases and hidden test support where appropriate.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### E-08 — Secure isolated execution.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** Docker-sandbox adapter exists, but real containment and Windows behavior are not yet verified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### E-09 — Docker-based execution with actual container verification.
**Status:** BLOCKED · **Previous:** BLOCKED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** Docker CLI/engine unavailable on current Linux host; real container test not executed.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Run on compatible Windows/runner or hardware with required dependencies, record evidence and fix failures.

### E-10 — Execution disabled safely when isolation is unavailable.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### E-11 — SQL editor and query execution.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### E-12 — Frontend implementation practice.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### E-13 — DSA and competitive programming support.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### E-14 — System design and diagram assistance.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/code_runner.py; services/ai_worker/app/sql_lab.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_docker_command_enforces_isolation [mock Docker]; test_upgrade.py::test_sql_joins
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### F-01 — Single-select and multiple-select MCQs.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### F-02 — Numerical-answer questions.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### F-03 — Assertion-reason questions.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### F-04 — Code-output questions.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### F-05 — Image-based questions.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** Images can be OCR-extracted into text but image-based MCQ schema and scoring are not implemented.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### F-06 — Section-based assessments.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### F-07 — Configurable timers.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### F-08 — Negative marking.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### F-09 — Cutoff and scoring rules.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** Negative marking and points supported; cutoff and sectional pass thresholds missing.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### F-10 — Navigation and question review.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### F-11 — Autosave and recovery after interruption.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### F-12 — Final submission and result generation.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### F-13 — Accuracy, speed and topic-wise analytics.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/logic.py; apps/desktop/src/views/Assessments.tsx; services/ai_worker/app/db.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v05.py::test_multi_numeric_assessment_end_to_end, test_v05.py::test_mixed_scoring_negative_and_missing
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-01 — DSA and problem-solving interviews.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-02 — Core CS subjects: OS, DBMS, CN and OOP.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-03 — Java, Python, C++, JavaScript and frontend interviews.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-04 — SQL and database interviews.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-05 — Data Analyst and Business Analyst interviews.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### G-06 — Machine Learning breadth and depth.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-07 — ML mathematics and algorithms.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-08 — ML system design and scalable ML applications.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-09 — Resume-based and project-based interviews.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-10 — HR and behavioural interviews.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-11 — STAR-based answer evaluation.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### G-12 — Communication, listening and speaking assessments.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-13 — Reading and repetition exercises.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### G-14 — Jumbled-word and verbal exercises.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `apps/desktop/src/App.tsx; apps/desktop/src/views/Live.tsx; services/ai_worker/app/providers.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_fake_stream_persists [mock provider]; no specialist end-to-end test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### H-01 — PDF and DOCX parsing.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_parse_upload_documents; no full resume follow-up test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### H-02 — Resume information extraction.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_parse_upload_documents; no full resume follow-up test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### H-03 — Project and experience indexing.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_parse_upload_documents; no full resume follow-up test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### H-04 — Retrieval from candidate-provided documents.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_parse_upload_documents; no full resume follow-up test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### H-05 — Resume-specific question generation.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_parse_upload_documents; no full resume follow-up test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### H-06 — Project-specific follow-up questions.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_parse_upload_documents; no full resume follow-up test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### H-07 — Candidate response evaluation.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_parse_upload_documents; no full resume follow-up test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### H-08 — Missing concepts and improvement suggestions.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_parse_upload_documents; no full resume follow-up test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### H-09 — Protection against unsupported claims in generated answers.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_parse_upload_documents; no full resume follow-up test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### I-01 — Mock interview session summaries.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_assessment; test_v05.py::test_multi_numeric_assessment_end_to_end
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### I-02 — Topic-wise performance.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_studio.py::test_assessment; test_v05.py::test_multi_numeric_assessment_end_to_end
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### I-03 — Response quality assessment.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_assessment; test_v05.py::test_multi_numeric_assessment_end_to_end
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### I-04 — Missed concepts and weak areas.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_assessment; test_v05.py::test_multi_numeric_assessment_end_to_end
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### I-05 — Coding performance analytics.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_assessment; test_v05.py::test_multi_numeric_assessment_end_to_end
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### I-06 — Time management analysis.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_assessment; test_v05.py::test_multi_numeric_assessment_end_to_end
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### I-07 — Improvement plans.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_assessment; test_v05.py::test_multi_numeric_assessment_end_to_end
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### I-08 — Historical session comparison.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_assessment; test_v05.py::test_multi_numeric_assessment_end_to_end
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### I-09 — Exportable reports.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_studio.py::test_assessment; test_v05.py::test_multi_numeric_assessment_end_to_end
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### J-01 — CPU and RAM monitoring.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### J-02 — Resource-budget configuration.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### J-03 — Model selection based on available hardware.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### J-04 — Model downgrade and fallback mechanisms.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** A usable, end-to-end feature is absent.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### J-05 — Concurrent task limits.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### J-06 — Audio and inference resource management.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### J-07 — Background worker lifecycle.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### J-08 — Cancellation and cleanup.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### J-09 — Context and memory optimization.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### J-10 — Startup and idle resource measurements.
**Status:** BLOCKED · **Previous:** BLOCKED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** External Windows hardware, npm/Rust toolchains, Docker or real provider access needed.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Run on compatible Windows/runner or hardware with required dependencies, record evidence and fix failures.

### J-11 — Performance benchmarks on the target Windows laptop.
**Status:** BLOCKED · **Previous:** BLOCKED
**Source:** `services/ai_worker/app/resources.py; services/ai_worker/app/main.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The specified i5-1145G7 target laptop is not accessible.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_upgrade.py::test_resource_profile_persists; no target laptop test
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Run on compatible Windows/runner or hardware with required dependencies, record evidence and fix failures.

### K-01 — Secure API-key storage.
**Status:** IMPLEMENTED — NOT VERIFIED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/credentials.py; services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** v0.6 Python test_v06.py contract tests (mocked external providers); no real Windows vault or cloud-provider validation.
**Gap:** Real Windows credential-vault test and live-provider end-to-end verification remain; no automatic cloud fallback, and billed token usage is not available.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Validate Windows Credential Manager with a real user account; exercise real cloud provider with user-owned credentials and measure latency/usage.

### K-02 — Per-launch worker authentication.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### K-03 — Dynamic local ports and authenticated communication.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### K-04 — Input validation.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### K-05 — IPC authorization.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### K-06 — Restricted filesystem access.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### K-07 — Safe code execution.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### K-08 — Database and file protection.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### K-09 — Explicit permissions and recording indicators.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### K-10 — Configurable retention and deletion.
**Status:** TESTED — DEFINED CODE-PATH · **Previous:** TESTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** Local Python suite: 60 passed, 2026-11-02; see docs/V05_TEST_REPORT.json
**Gap:** End-to-end Windows UI/device validation may still be required.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Complete full cross-layer and Windows acceptance testing.

### K-11 — No unnecessary raw audio retention.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### K-12 — Dependency and vulnerability checks.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/main.py; apps/desktop/src-tauri/src/lib.rs; services/ai_worker/app/code_runner.py`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### K-13 — Safe logging without exposing secrets.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `services/ai_worker/app/credentials.py; services/ai_worker/app/providers.py; services/ai_worker/app/main.py; services/ai_worker/app/db.py; apps/desktop/src/views/Tools.tsx`
**Evidence:** v0.6 Python test_v06.py contract tests (mocked external providers); no real Windows vault or cloud-provider validation.
**Gap:** Real Windows credential-vault test and live-provider end-to-end verification remain; no automatic cloud fallback, and billed token usage is not available.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: test_v03.py::test_worker_token_required, test_upgrade.py::test_sql_read_only, test_v05.py::test_transcript_deletion_cascades_with_session
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Validate Windows Credential Manager with a real user account; exercise real cloud provider with user-owned credentials and measure latency/usage.

### L-01 — Windows installer.
**Status:** BLOCKED · **Previous:** BLOCKED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** Historical v0.5 CI and installation smoke passed; no v0.6 binary has been built or tested.
**Gap:** New version v0.6 must be built and installed; v0.5 installer must not be relabeled.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Run on compatible Windows/runner or hardware with required dependencies, record evidence and fix failures.

### L-02 — Portable Windows package.
**Status:** BLOCKED · **Previous:** BLOCKED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** Historical v0.5 CI and installation smoke passed; no v0.6 binary has been built or tested.
**Gap:** New version v0.6 must be built and installed; v0.5 installer must not be relabeled.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Run on compatible Windows/runner or hardware with required dependencies, record evidence and fix failures.

### L-03 — Clean installation.
**Status:** BLOCKED · **Previous:** BLOCKED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** Historical v0.5 CI and installation smoke passed; no v0.6 binary has been built or tested.
**Gap:** New version v0.6 must be built and installed; v0.5 installer must not be relabeled.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Run on compatible Windows/runner or hardware with required dependencies, record evidence and fix failures.

### L-04 — Upgrade from previous version.
**Status:** NOT IMPLEMENTED · **Previous:** NOT IMPLEMENTED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** No v0.4 -> v0.5 upgrade validation.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement a scoped feature and automated test before exposing it as supported.

### L-05 — Uninstallation and data-retention behaviour.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### L-06 — Worker startup and shutdown.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### L-07 — Offline and network-failure behaviour.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### L-08 — Application recovery after crash.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### L-09 — Actual end-to-end Windows tests.
**Status:** BLOCKED · **Previous:** BLOCKED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** v0.4 smoke tests exist; v0.5 has not been built or validated on Windows.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Run on compatible Windows/runner or hardware with required dependencies, record evidence and fix failures.

### L-10 — Release documentation and checksums.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** PARTIALLY IMPLEMENTED
**Source:** `.github/workflows/windows-release.yml; scripts/build.ps1; docs/V04_WINDOWS_CI_RESULTS.json`
**Evidence:** No full v0.5 acceptance evidence; see docs/TESTING_AND_ACCEPTANCE.md
**Gap:** The complete user workflow or production integration is incomplete/unverified.
**Acceptance:** Implement the complete behavior described by the requirement, then verify it across supported components, persistence, recovery and appropriate Windows hardware where relevant.
**Automated test:** Relevant partial/mocked checks: GitHub Actions v0.4 run 41349734490 (historical only); no v0.5 Windows run
**Manual verification:** On a clean Windows installation, exercise this requirement through the desktop UI, verify outputs/persistence/errors and record evidence; for hardware-dependent items use supported devices.
**Next action:** Implement missing behavior, connect UI/backend, and add acceptance tests.

### M-001 — Multimodal normalization of typed text, screenshots, diagrams, tables, code and mathematical notation into a common question representation.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `services/ai_worker/app/main.py`
**Evidence:** PDF master specification p.17–18; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Multimodal normalization of typed text, screenshots, diagrams, tables, code and mathematical notation into a common question representation.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-002 — OCR quality indication and uncertainty for unreadable diagrams, mathematics and code in screenshots.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `services/ai_worker/app/main.py`
**Evidence:** PDF master specification p.18; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** OCR quality indication and uncertainty for unreadable diagrams, mathematics and code in screenshots.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-003 — Explicitly authorized browser content integration via supported browser APIs/extensions.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `apps/desktop/src/App.tsx`
**Evidence:** PDF master specification p.18; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Explicitly authorized browser content integration via supported browser APIs/extensions.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-004 — Dedicated mathematical derivation and notation rendering during ML practice.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `apps/desktop/src/App.tsx`
**Evidence:** PDF master specification p.27–28; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Dedicated mathematical derivation and notation rendering during ML practice.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-005 — Editable, inspectable structured resume knowledge graph with claims versus evidence.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `services/ai_worker/app/db.py`
**Evidence:** PDF master specification p.29–30; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Editable, inspectable structured resume knowledge graph with claims versus evidence.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-006 — Optional simulated interviewer workflow with structured STAR scoring based on supplied real examples.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `apps/desktop/src/App.tsx`
**Evidence:** PDF master specification p.30–31; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Optional simulated interviewer workflow with structured STAR scoring based on supplied real examples.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-007 — Listening/repeating exercise with a reference audio sample and transcript comparison, including omissions/reorders.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `apps/desktop/src/views/Tools.tsx`
**Evidence:** PDF master specification p.31; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Listening/repeating exercise with a reference audio sample and transcript comparison, including omissions/reorders.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-008 — Interactive jumbled-word practice accepting alternative grammatically correct arrangements.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `apps/desktop/src/views/Tools.tsx`
**Evidence:** PDF master specification p.31; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Interactive jumbled-word practice accepting alternative grammatically correct arrangements.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-009 — Desktop overlay configurable click-through, answer pinning and previous-answer navigation on supported OS APIs.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `apps/desktop/src-tauri/src/lib.rs`
**Evidence:** PDF master specification p.36; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Desktop overlay configurable click-through, answer pinning and previous-answer navigation on supported OS APIs.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-010 — Onboarding and separate troubleshooting/about pages with tested settings and diagnostics workflows.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `apps/desktop/src/App.tsx`
**Evidence:** PDF master specification p.37; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Onboarding and separate troubleshooting/about pages with tested settings and diagnostics workflows.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-011 — Signed update verification and upgrade authenticity checks, without unverified auto-replacement.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `apps/desktop/src-tauri/tauri.conf.json`
**Evidence:** PDF master specification p.41; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Signed update verification and upgrade authenticity checks, without unverified auto-replacement.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-012 — First-useful-answer and cancellation-latency benchmarks distinct from first-token latency.
**Status:** PARTIALLY IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `services/ai_worker/app/main.py`
**Evidence:** PDF master specification p.41–42; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** First-useful-answer and cancellation-latency benchmarks distinct from first-token latency.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-013 — Frontend implementation live preview with accessibility/responsiveness checks and controlled modifications.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `apps/desktop/src/views/Tools.tsx`
**Evidence:** PDF master specification p.24; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** Frontend implementation live preview with accessibility/responsiveness checks and controlled modifications.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.

### M-014 — User-authorized screen-capture compatibility diagnostics that do not bypass monitoring or proctoring.
**Status:** NOT IMPLEMENTED · **Previous:** NOT AUDITED IN V0.5
**Source:** `scripts/mock-capture-test.ps1`
**Evidence:** PDF master specification p.36; requirement extracted from original specification, not implementation evidence
**Gap:** Full integrated implementation and evidence remain outstanding.
**Acceptance:** User-authorized screen-capture compatibility diagnostics that do not bypass monitoring or proctoring.
**Automated test:** Not run
**Manual verification:** Create an authorized practice scenario exercising this complete requirement on real Windows hardware.
**Next action:** Implement narrowly, add tests and user-facing controls before verification.
