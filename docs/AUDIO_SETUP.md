# Optional speech-to-text setup

Install optional worker dependency on your Windows development environment:

```powershell
.\services\ai_worker\.venv\Scripts\python.exe -m pip install -r .\services\ai_worker\requirements-stt.txt
```

In `Live practice`, click **Record microphone**, grant browser/WebView microphone permission, record a short practice question and click **Stop microphone**. The clip is sent to your own loopback worker. `faster-whisper` lazily loads the model configured by `STT_MODEL` (default `tiny`) and returns text plus timestamped segments. The model may download weights on first use; allow disk space and inform other local users before downloading. CPU-only int8 is used by default. The microphone icon is not a continuous recording indicator after you stop; raw audio is not saved to SQLite.

**Language:** the endpoint accepts `language=auto`, `en` or `hi` as a query string; available accuracy depends on the chosen Whisper model, microphone and audio quality. Hinglish is not independently benchmarked. **Speaker distinction:** response uses `speaker: unknown`, because the application cannot reliably attribute multiple people in mixed audio to interviewer/candidate. There is no finished system-audio loopback or continuous dual-source capture in this preview.

**Troubleshooting:** verify the OS microphone permission, input levels, accepted audio format (`webm`, `wav`, `mp3`, `ogg`, `m4a`) and optional model package. If model loads fail, choose a smaller model or disable STT. Review transcript before using it as a practice question.
