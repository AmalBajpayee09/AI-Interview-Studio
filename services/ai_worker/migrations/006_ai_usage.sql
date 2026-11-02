-- Incremental migration 5 -> 6. Executed transactionally by db.initialize().
CREATE TABLE IF NOT EXISTS ai_usage (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    provider TEXT NOT NULL, model TEXT NOT NULL,
    first_token_ms INTEGER, total_ms INTEGER NOT NULL,
    output_characters INTEGER NOT NULL, created REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS ai_usage_by_session ON ai_usage(session_id,created);
