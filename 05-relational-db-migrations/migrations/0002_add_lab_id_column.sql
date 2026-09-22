-- Migration 0002: add lab_id — step 1 of a safe, three-step column addition.
--
-- Why not just add it as NOT NULL in one go? Because on a table with existing rows,
-- that either fails outright or locks the table while every row gets a default value —
-- fine on a demo table, a real problem on a production table with real traffic.
-- The safe pattern is: (1) add nullable, (2) backfill, (3) enforce NOT NULL — see 0003 and 0004.
-- UP

ALTER TABLE readings ADD COLUMN lab_id TEXT;  -- nullable on purpose, for now

-- DOWN (for rollback)
-- SQLite can't drop a column directly pre-3.35; Postgres/Fabric: ALTER TABLE readings DROP COLUMN lab_id;
