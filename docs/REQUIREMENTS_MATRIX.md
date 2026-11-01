# Original 58-page requirement status summary — preview 0.1.0

Retained original specification: `USER_REQUIREMENTS.pdf`. This matrix is **not** a release approval. Any unsupported or untested item remains open. No feature is claimed merely because a navigation button exists.

| Specification section(s) | Implementation status | Evidence / missing items |
| --- | --- | --- |
| 0/1 Product goals, output artifacts | Partial | Source repository and ZIP; working API/browser companion; native installer not generated. |
| 2 Hardware profiles, resource governor | Partial | `GET /api/diagnostics` reports actual memory, CPU and suggested profile. No predictive governor/cooldowns/GPU verification. |
| 3/4/5 Technology, HLD/LLD/contracts | Source implemented, native untested | React/Tauri, worker, SQLite schemas and shared contracts. Rust build not executed. |
| 6 Real-time audio, diarization, latency | Partial | Manual microphone recording + optional batch faster-whisper endpoint. No continuous STT, system-audio loopback or reliable dual-speaker separation. |
| 7 Multimodal / OCR | Partial | File upload extraction for PDF/DOCX/text/image OCR. No direct automatic window capture or guaranteed semantic diagram reading. |
| 8 MCQ intelligence | Partial | Deterministic grading of sample/user-defined quiz. LLM explanation available through practice; robust image MCQ extraction limited by OCR. |
| 9 Timed assessments | Partial | Timer/navigation/review in React, basic timer/navigation in companion, score reports. No multi-round builder or tamper-proof recovery. |
| 10 Coding/DSA engine | Partial | Python AST syntax validation, practice prompts. No safe code execution or hidden-test guarantee; other language syntax validation disabled. |
| 11/12 Frontend and SQL assistance | AI prompt workflow only | No dedicated validated SQL runner or frontend artifact renderer. |
| 13 System design | Partial | Domain prompts, context and model responses; no validated Mermaid generation. |
| 14/15 ML interviews & system design | Partial | Specialized prompts and model answers; no formal equation verifier. |
| 16 Resume/project knowledge | Partial | PDF/DOCX/text/notes ingestion, lexical contextual retrieval, deletion. No full entity graph. |
| 17 Behavioural/HR | Partial | Model-assisted coaching, context; no validated scoring rubric. |
| 18 Communication | Partial | Transcript WPM and filler metrics, optional microphone transcription; no pronunciation/pause alignment. |
| 19/20 Answer modes and confidence | Partial | Seven modes, verification explicitly marked absent. No probabilistically calibrated confidence. |
| 21 Model routing | Partial | User-selectable Ollama/cloud; classification exists. No smart capability/latency routing. |
| 22 Local/cloud/offline | Partial | Ollama and explicit cloud adapters written, not live-tested here. Offline quiz works. |
| 23 Overlay/window | Source-only | Standard compact always-on-top Tauri command, not Windows tested; no stealth/undetectability/bypass. |
| 24 UI | Source + browser companion | React premium screens and working fallback companion. React build not verified; some features partial. |
| 25 Sessions/context/memory | Implemented baseline | SQLite persistence, export/delete, bounded recent turns and document snippets. No adaptive summarization. |
| 26 Analytics | Implemented baseline | Counts, avg latency and quiz score. No psychometric or strong error diagnosis. |
| 27 Security | Partial | Loopback, host/origin checks, no code execution, cloud opt-in. No credential vault or authenticated IPC. |
| 28 Performance | Partial | Actual Python microbenchmarks. No model/audio/UI native benchmarks. |
| 29 Testing | Partial | Python automated tests executed; Windows/Rust/frontend E2E not run. |
| 30 Repository structure | Implemented with adjustments | Maintained source, docs, scripts, shared contract reference. |
| 31/32 Beginner setup/troubleshooting | Written, Windows unverified | Windows instructions and common diagnosis guide. |
| 33–37 Roadmap, definition of done and release | Partially achieved | Source archive verified, tests and metrics recorded. Windows release blockers remain. |

## Excluded capabilities

This project does not modify Safe Exam Browser to evade restrictions or monitoring, hide from other participants, manipulate endpoint alerts, or covertly disable security policies. Its visible mock overlay uses ordinary OS window behaviors and must be used under organizer-authorized conditions.
