# v0.9 session continuity acceptance evidence

- Python `test_v09.py::test_followup_context_and_order_recovered_after_db_reopen`: **PASS** with a **simulated provider**, asserting prior user/assistant messages are included in the next request, turn ordering is retained and SQLite reopen preserves turns.
- `test_v09.py::test_cancel_then_retry_does_not_duplicate_or_save_partial`: **PASS** with a **simulated provider**, verifying cancelled responses are discarded and only a completed retry persists.
- `test_v09.py::test_real_subprocess_auth_database_and_restart`: **PASS on Linux**, launching an actual network worker twice with the same SQLite directory, verifying the token gate, session recovery and allowlisted startup event logs. No AI inference is performed.
- `test_v09.py::test_real_ollama_api_stream_and_followup`: **SKIPPED by default**, requires a real installed Ollama and a pulled model. Running this successfully would validate live HTTP/SQLite continuity, but not the Tauri desktop UI.
- Full Windows desktop + live Ollama + cancellation + app restart + recovery: **NOT VERIFIED**. Requires physical/model-enabled Windows acceptance and actual performance capture.

No database schema changes were needed for this milestone: SQLite `user_version=5` remains intact, and no existing tables or user turns are cleared by the new worker lifecycle code.
