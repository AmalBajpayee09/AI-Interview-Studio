-- v0.12 transactional migration; old attempts and sessions preserved.
CREATE TABLE IF NOT EXISTS attempt_receipts (
 assessment_id TEXT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
 started REAL NOT NULL,
 attempt_id TEXT NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
 PRIMARY KEY (assessment_id, started)
);
CREATE INDEX IF NOT EXISTS receipts_by_attempt ON attempt_receipts(attempt_id);
PRAGMA user_version=6;
