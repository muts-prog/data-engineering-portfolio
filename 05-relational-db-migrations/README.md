# 05 — Relational Database & Safe Migrations

**JD line this targets:** "In-depth knowledge and comfortable working with relational
databases (MySQL, PostgreSQL) ... including building, optimizing, debugging, and creating
queries and safe migration scripts."

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

## Why this matters (be ready to explain it, not just run it)

Adding a `NOT NULL` column in one step either fails against existing rows or locks the table
while a default gets applied to all of them. Splitting it into expand → backfill → contract
is the standard safe pattern used in real migration tools (Alembic, Flyway, Django migrations).

## To make this real

- Run the same four scripts against a real **PostgreSQL** or **Azure SQL** database — the SQL
  is close to standard; only the SQLite-specific table-rebuild in 0004 needs to change to a
  simple `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`.
- Optional: wrap this in **Alembic** (Python) so migrations are version-tracked automatically
  rather than run by hand — worth doing if you want a stronger DevOps story.

## How to describe this on your CV

> Wrote and tested a multi-step, zero-downtime-style database migration (expand → backfill →
> constrain) against a table with existing data. [GitHub link]
