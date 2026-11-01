-- Reference migration, equivalent applied automatically in db.initialize().
CREATE INDEX IF NOT EXISTS session_updated ON sessions(updated DESC);
