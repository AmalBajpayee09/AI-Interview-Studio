# Experimental live audio sources (v0.3)

Backend module: `services/ai_worker/app/audio_live.py`. Two independently selected `SoundCard` recording sources are supported when the local OS backend provides them. On Windows, loopback microphone devices may correspond to WASAPI system/playback sources; availability depends on hardware and permissions. Audio capture is explicitly started by the user and a prominent recording indicator is shown.

Install optional dependencies for source builds:

```powershell
& .\services\ai_worker\.venv\Scripts\python.exe -m pip install -r services\ai_worker\requirements-stt.txt
```

Then use **Live practice > Continuous audio transcription**. Refresh devices, choose one or two distinct sources, choose auto/English/Hindi, and start recording. Generated transcript events include source ID, unknown speaker, language, and STT latency. Review before using text in a question. Optional auto-append does not auto-submit the question to a provider. Microphone audio is not saved to the database.

The voice gate uses bounded RMS-and-silence-based chunks (16 sec maximum); this is not equivalent to advanced VAD or diarization. STT uses a lazily loaded CPU `faster-whisper` tiny model by default and finalized transcripts; model downloads must be separately authorized and may be slow. No reliable speaker identity is inferred from microphone versus system source. Mixed audio, browser conferencing mixes, accents and Hinglish can cause transcription errors. A genuine diarization model and correction-capable partial streaming are not implemented.

No SoundCard installation, physical audio endpoint, or real Whisper run was available in this Linux build environment. Unit tests cover segmentation and event contracts only. Windows real-device testing, device reconnection, bilingual transcription and actual latency measurements are pending.
