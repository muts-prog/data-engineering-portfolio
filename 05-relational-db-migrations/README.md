# 05 — Relational Database & Safe Migrations

## What's here

Four numbered migrations that build a table, then evolve it — showing the **safe** way to
add a required column to a table that already has data, not just the naive one-step way:

1. `0001_create_readings_table.sql` — initial table, with a `CHECK` constraint
2. `0002_add_lab_id_column.sql` — adds the new column as **nullable**
3. `0003_backfill_lab_id.sql` — fills in existing rows
4. `0004_enforce_lab_id_not_null.sql` — only now enforces `NOT NULL`

`run_migrations.py` applies them in order against a fresh SQLite database, inserting rows
*between* migrations 1 and 2 to prove the pattern survives real, pre-existing data.

Run:
```
python run_migrations.py
```
