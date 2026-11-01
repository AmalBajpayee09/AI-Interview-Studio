# User guide — source preview v0.2.0

**Start:** Read `WINDOWS_SETUP.md` and run `scripts/run-browser.ps1` to access the HTTP-based companion. A native `.exe` has not yet been compiled.

**Practice session:** Enter your question, choose Ollama or explicitly enabled cloud, pick answer depth, then start streaming. Saved question/answer context is per session. Model output is unverified unless it explicitly reports external checking.

**Assessments:** Choose an assessment. A new quiz starts a timer; answers and marked questions are autosaved to the local SQLite draft table, and the same assessment can be resumed after restarting. Submitted scores are final, and draft data is removed. These are practice timers, not tamper-proof exam timers.

**SQL lab:** Use the built-in practice database; see `SQL_PRACTICE.md`. Only SELECT/WITH query reads are permitted. Do not attempt to connect any outside database.

**Coding:** Python syntax validation parses source without executing it. AI feedback is available if your configured provider is running. Code execution/hidden test verification is not available.

**Documents:** Upload your own PDF/DOCX/TXT or OCR-supported images; verify extracted text before saving. AI may retrieve matching excerpts for future practice.

**Speech:** Existing microphone flow records a segment and uploads it for STT when optional faster-whisper is installed. No always-listening or guaranteed speaker separation. Recording status is visible and audio is not saved to the database.

**Backup:** In Settings choose `Download SQLite backup` or use `/api/backup/database` while the worker is running. To restore, **first stop the worker** then run from PowerShell:

```powershell
py -3.11 scripts/restore-database.py "C:\path\to\ai-interview-studio-backup.sqlite3"
```

This validates integrity and saves the existing DB as a dated `.bak` when applicable. SQLite backups contain sensitive practice answers/resume text; protect them.

**Resource modes:** Settings provides battery saver, balanced and performance recommendations. They influence advisory concurrency, not live model configuration or operating-system throttling.

**Privacy:** All sessions are local by default. Cloud AI sends question context only after explicit configuration and selection. Avoid using in unauthorized real assessments. Overlay works as a visible user-controlled practice tool, not a stealth application.
