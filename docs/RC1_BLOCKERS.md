# RC1 known limitations — production approval blocked

- This development host has no Windows OS, Rust/Cargo, Docker daemon, installed Ollama model/service, working audio device, or connected live cloud credentials; running Linux Python tests does not verify those capabilities.
- Existing Docker four-language isolation has genuine Linux CI evidence, but Windows Docker Desktop acceptance is missing.
- WAV activity detection is not STT/speaker diarization. No participant identity can be verified.
- Strict timed assessment is opt-in for new quizzes; legacy practice remains direct-submit. Section cutoffs and advanced image/assertion/code rubrics remain incomplete. UI restart and deadline tests need a real installed Windows build.
- No real Ollama first-token/total response latency or installed desktop cold-start/idle RAM collected.
- The workflow may package an older `0.9.0` app version until a dedicated, verified version bump; such artifacts must not be presented as a v1.0 installer.
- Pending Windows upgrade, uninstall/reinstall user-data retention, error/failure recovery and full system security review.

The target status is **NOT PRODUCTION READY** until all gates are recorded with actual evidence.
