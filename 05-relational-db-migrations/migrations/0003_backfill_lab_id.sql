-- Migration 0003: backfill lab_id for existing rows — step 2 of the safe column addition.
-- In a real system with millions of rows, this would run in batches (e.g. 10,000 rows at a
-- time in a loop) to avoid one giant long-running transaction locking the table. At demo
-- scale a single UPDATE is fine — the important part is knowing *why* batching matters at
-- scale, which is worth being able to explain even if this script doesn't need it.
-- UP

UPDATE readings SET lab_id = 'UNKNOWN' WHERE lab_id IS NULL;

-- DOWN (for rollback)
-- UPDATE readings SET lab_id = NULL WHERE lab_id = 'UNKNOWN';
