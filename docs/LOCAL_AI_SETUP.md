# Local model setup

Official Ollama downloads: https://ollama.com/download/windows. API specification: https://github.com/ollama/ollama/blob/main/docs/api.md

```powershell
ollama --version
ollama pull qwen2.5:3b
ollama list
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

Set `OLLAMA_URL=http://127.0.0.1:11434` and `OLLAMA_MODEL=qwen2.5:3b` in `.env`, then restart the worker. A 3B quantized model is a modest starting point for 16 GB RAM, not a guarantee: CPU performance, context length, accuracy and memory consumption vary across builds. Models are downloaded **only** by your explicit `ollama pull` command. To try a smaller compatible model, update the model name and pull it first.

The Python backend detects available model names from `/api/tags` and sends streaming requests to `/api/chat`. Currently it does not verify image capability or alternate accelerators. No GPU assertion is made. To measure your actual setup, time a real prompt and watch Windows Task Manager. Report downloaded model and request details alongside results.

Optional STT:

```powershell
.\services\ai_worker\.venv\Scripts\python.exe -m pip install -r .\services\ai_worker\requirements-stt.txt
```

Set `STT_MODEL=tiny` (fastest but weaker quality) or a compatible larger model if your CPU and memory can support it. Downloads require explicit action when configuring STT; loading an absent model may cause faster-whisper to fetch model weights when first used, so use it only after reviewing its download policy. Audio uses CPU INT8. Hindi/Hinglish accuracy must be checked empirically; no live streaming or diarization is promised.
