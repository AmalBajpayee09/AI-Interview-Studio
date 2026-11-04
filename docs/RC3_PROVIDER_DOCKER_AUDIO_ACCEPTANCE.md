# RC3 real provider, Docker Desktop, audio and resume acceptance — blocked gates

## Ollama and cloud providers — BLOCKED

No real Ollama service or pulled model is available on the development host. The application contains a local model catalogue, streaming provider adapter, cancellation and consent controls, but mock provider tests do not count as real inference. On a consenting Windows test machine, explicitly install and start Ollama, choose and pull a hardware-appropriate model (no automatic download), set `STUDIO_LIVE_OLLAMA_TEST=1` and `STUDIO_TEST_OLLAMA_MODEL=<model>`, then run `py -3.11 -m pytest services/ai_worker/tests/test_v09.py::test_real_ollama_api_stream_and_followup -q` with `PYTHONPATH=services/ai_worker`. Record Ollama version, exact model, computer RAM/CPU, real TTFT, total time, streaming, cancellation and restarted session. Also exercise the same route through the installed Windows desktop UI. Do not log private prompts or tokens.

Cloud inference remains unverified without explicit authorization, consent and configured OS-backed credentials. Check vault storage, rate limits, timeout, stream cancellation, model identity and context in a separate authorized test. No hidden automatic fallback.

## Docker Desktop on Windows — BLOCKED

Prior Linux Docker CI genuinely ran execution and isolation tests. It does **not** prove compatibility with Windows Docker Desktop. On a Windows machine using Docker Desktop Linux containers, deliberately test C++, Python, Java and JS jobs for network-off, non-root, CPU/memory/file/process caps, timeouts, malicious path attempts, bounded output, cancellation, daemon outages and cleanup. Never fall back to executing candidate code directly on the host.

## Windows audio and diarization — BLOCKED

No microphone/loopback device or consented multi-speaker recording is available. Real Windows acceptance requires user-visible recording indicator, explicit per-source consent, device selection, permissions, sample-rate/channel validation, speech and silence, disconnect/reconnect and transcript timestamps. Speaker identification must be described as *unknown* without sound evidence. Audio is never recorded secretly; raw audio retention is opt-in.

## Resume-to-mock-interview and analytics — PARTIAL

Resume parsing has source-linked sections and security bounds; the complete installed UI resume upload → verified extraction → contextual questions → real model follow-up → saved report flow remains unverified. No personal resume content was used in RC3 CI; use synthetic consented data. Objective scores and subjective AI feedback must remain differentiated.
