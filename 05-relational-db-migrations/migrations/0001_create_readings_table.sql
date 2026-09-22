-- Migration 0001: create the readings table.
-- UP

BEGIN TRANSACTION;

CREATE TABLE readings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,  -- Postgres: SERIAL / GENERATED ALWAYS AS IDENTITY
    sample_id       TEXT NOT NULL UNIQUE,
    county          TEXT NOT NULL,
    crop            TEXT NOT NULL,
    aflatoxin_ppb   REAL NOT NULL CHECK (aflatoxin_ppb >= 0),
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

COMMIT;

-- DOWN (for rollback)
-- DROP TABLE readings;
