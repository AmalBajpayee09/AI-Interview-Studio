# Performance report — v0.5.0

Actual local figures come from `docs/V05_BENCHMARK.json`, measured 2026-11-02 on a **Linux x86_64** container with Python 3.13.5, 5 logical CPUs, 5.81 GiB total RAM. FastAPI requests use in-process `TestClient`: values are *not* network ping, desktop UI latency, or AI model latency.

| In-process operation | Samples | p50 (ms) | p95 (ms) |
|---|---:|---:|---:|
| in_process_http_health | 120 | 0.956 | 2.149 |
| in_process_sql_select | 50 | 2.234 | 5.147 |
| in_process_sql_join | 50 | 3.211 | 12.91 |
| in_process_db_session_create | 30 | 4.991 | 6.532 |

Measured Python process RSS after these operations: **113.3 MiB** (not total desktop app RAM).

**NOT MEASURED:** Windows cold/warm startup, Tauri+React idle/peak CPU/RAM, first-token and full-answer latency, real microphone or STT processing, genuine Docker execution, or the target i5-1145G7 16-GB Windows laptop. No 1–2 second answer guarantee is supported by this data.

Suggested Windows benchmarks: launch packaged exe after reboot, poll actual health/worker startup, measure memory in Windows Process Explorer, audio start → final transcript for both sources, local model streaming TTFT and full output by model, and real Docker execution latency under CPU/RAM constraints. Report p50/p95 with sample counts.
