# Dependencies and licensing overview

**Application source:** project-created MIT code in `LICENSE`. The supplied Safe Exam Browser reference archive was inspected in the earlier source preview and is not distributed within this source ZIP; it retains its own licenses.

**Frontend:** React, React DOM, Vite, TypeScript and Tauri 2 API/CLI, declared in `apps/desktop/package.json`. **Desktop:** Rust `tauri`, `serde`, `serde_json` in `apps/desktop/src-tauri/Cargo.toml`. **Worker:** FastAPI, Uvicorn, httpx, Pydantic, python-multipart, psutil, PyMuPDF, python-docx, Pillow, pytesseract, pytest in `requirements.txt`; optional faster-whisper in `requirements-stt.txt`; optional Windows PyInstaller in `scripts/build.ps1`. Their respective package licenses apply and must be audited during release verification.

No model weights, paid API credentials, bundled CPython runtime or third-party SEB code are included in this source ZIP. Ollama downloads and licenses depend on the selected model. The Windows installer must be built and checked on Windows before redistribution. This is a dependency summary, **not** a completed third-party license audit.
