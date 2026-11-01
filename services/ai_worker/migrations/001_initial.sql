-- Reference schema. The equivalent migration is executed in app/db.py.
CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, title TEXT NOT NULL, created REAL NOT NULL, updated REAL NOT NULL);
CREATE TABLE IF NOT EXISTS turns (id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE, question TEXT NOT NULL, answer TEXT NOT NULL, mode TEXT NOT NULL, provider TEXT NOT NULL, elapsed_ms INTEGER NOT NULL, created REAL NOT NULL);
CREATE INDEX IF NOT EXISTS turns_by_session ON turns(session_id,created);
CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, filename TEXT NOT NULL, content TEXT NOT NULL, created REAL NOT NULL);
CREATE TABLE IF NOT EXISTS assessments (id TEXT PRIMARY KEY, title TEXT NOT NULL, questions_json TEXT NOT NULL, duration_seconds INTEGER NOT NULL, created REAL NOT NULL);
CREATE TABLE IF NOT EXISTS attempts (id TEXT PRIMARY KEY, assessment_id TEXT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE, answers_json TEXT NOT NULL, started REAL NOT NULL, finished REAL, result_json TEXT);
