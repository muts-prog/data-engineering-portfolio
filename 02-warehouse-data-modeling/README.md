# 02 — Warehouse & Dimensional Data Modeling

**JD line this targets:** "Experience or deep understanding of data architecture and data
modelling."

## What's here

- `sql/schema_dimensional_model.sql` — a star schema (one fact table, four dimensions) for
  the aflatoxin data, with primary/foreign keys and indexes explained.
- `sql/load_and_query.py` — builds it in SQLite, loads it from the clean data produced in
  folder 01, and runs two analytical queries to prove the model actually answers real
  questions ("which counties are worst?", "is it trending up or down?").

Run:
```
cd sql
python load_and_query.py
```

## To make this real in Fabric / Azure

1. Recreate the same schema in a **Fabric Warehouse** (T-SQL, near-identical syntax) or an
   **Azure SQL Database**.
2. Load it via a **Fabric Data Pipeline** or **Data Factory** copy activity instead of the
   Python script — that's the part that's actually "production," not the schema design itself.
3. Build one Power BI report on top of the warehouse (not the raw table) — this is what
   "data architecture that's ready for analysis" looks like in practice.

## How to describe this on your CV

> Designed a star-schema data warehouse (fact + dimension tables) for research monitoring
> data and built the queries and load logic behind it. [GitHub link]

If you complete step 1–3 in Fabric/Azure for real, it's fair to say "in Microsoft Fabric" —
until then, keep the claim to the modeling and SQL itself.
