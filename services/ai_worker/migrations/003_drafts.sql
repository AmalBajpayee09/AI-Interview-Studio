-- Applied idempotently by app/db.py when PRAGMA user_version < 3.
CREATE TABLE IF NOT EXISTS assessment_drafts (
 assessment_id TEXT PRIMARY KEY REFERENCES assessments(id) ON DELETE CASCADE,
 answers_json TEXT NOT NULL,
 review_json TEXT NOT NULL,
 started REAL NOT NULL,
 updated REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS drafts_by_updated ON assessment_drafts(updated DESC);
