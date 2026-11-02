-- Version 5: optional session-bound transcript records. No raw audio.
-- Applied transactionally in app/db.py initialize(), not independently at runtime.
CREATE TABLE IF NOT EXISTS transcript_segments (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  text TEXT NOT NULL,
  source_id TEXT NOT NULL,
  speaker TEXT NOT NULL DEFAULT 'unknown',
  speaker_confidence REAL,
  language TEXT,
  started_at REAL,
  ended_at REAL,
  created REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS transcripts_by_session ON transcript_segments(session_id,created,id);
PRAGMA user_version=5;
