# Performance notes and honest measurements

`BENCHMARK.json` contains actual results measured **inside the provided Linux build container**, not on the target i5 laptop. It runs 250 in-memory question-classification calls and 80 in-process HTTP health calls. p50/p95 reflect those microbenchmarks only and exclude network, model loading, audio capture, speech recognition, UI rendering, and user hardware differences. They cannot establish the 1–2 second first-useful-answer target.

Benchmark hardware: approx. 5.81 GiB reported RAM; CPU brand not available. A Python process after FastAPI import used ~112 MB RSS in this sample. The target laptop (i5-1145G7, 16 GB RAM, Iris Xe) was **not accessible**. No GPU acceleration, STT audio latency, native startup time, LLM token latency or sustained Windows desktop memory was measured.

To reproduce:

```powershell
cd .\services\ai_worker
.\.venv\Scripts\python.exe bench.py
```

Goal for follow-up work: measure model warm-up, STT transcript latency, useful-answer p50/p95, cancellation, peak RAM and CPU on actual Windows laptop over long sessions. Adopt on-demand model loading and bounded CPU usage based on those results, not guessed GPU support.

## v0.2.0 measurements

See `BENCHMARK_V02.json` for measured native localhost HTTP GET (120 samples), SQLite training queries (300 samples) and classification (500 samples). These results are from Linux Python 3.13.5 with approximately 5.81 GiB total RAM and are **not** LLM answer or audio latencies. Current Windows baseline hardware was unavailable.
