-- Applied by app/db.py when PRAGMA user_version < 4.
CREATE TABLE IF NOT EXISTS settings (name TEXT PRIMARY KEY, value TEXT NOT NULL);
