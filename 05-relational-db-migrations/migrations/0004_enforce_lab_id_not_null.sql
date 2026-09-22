-- Migration 0004: enforce NOT NULL on lab_id — step 3 of the safe column addition.
--
-- On Postgres, Fabric Warehouse, or Azure SQL this is a one-liner now that every row is
-- backfilled:
--   ALTER TABLE readings ALTER COLUMN lab_id SET NOT NULL;
--
-- SQLite has no ALTER COLUMN at all, so enforcing a constraint means the classic
-- "rebuild the table" pattern below — worth knowing because some real migration
-- tools (including early Rails/Django migrations on SQLite) do exactly this under the hood.
-- UP

BEGIN TRANSACTION;

CREATE TABLE readings_new (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id       TEXT NOT NULL UNIQUE,
    county          TEXT NOT NULL,
    crop            TEXT NOT NULL,
    aflatoxin_ppb   REAL NOT NULL CHECK (aflatoxin_ppb >= 0),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    lab_id          TEXT NOT NULL
);

INSERT INTO readings_new SELECT * FROM readings;

DROP TABLE readings;
ALTER TABLE readings_new RENAME TO readings;

COMMIT;

-- DOWN (for rollback)
-- Re-run 0001-0003 against a fresh table, or restore from a pre-migration backup —
-- true rollback of a table rebuild is why you always back up before running this in production.
