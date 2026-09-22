# 06 — JSON / Non-Relational Data

**JD line this targets:** "Nonrelational data (JSON format) including building, optimizing,
debugging, and creating queries."

## What's here

- `schema/reading_document_schema.json` — a JSON Schema for a reading document, where
  `metadata` is deliberately loose because different collection methods capture different
  extra fields (GPS, multiple sensor readings, a review flag) — the exact situation where
  forcing everything into fixed table columns means a lot of NULLs.
- `schema/sample_documents.json` — three sample documents, each shaped slightly differently.
- `scripts/validate_and_query.py` — validates every document against the schema (catching
  malformed ones), then loads them into SQLite's JSON1 extension and queries into the nested
  structure with plain SQL — a fair stand-in for how Cosmos DB / MongoDB querying feels.

Run:
```
python scripts/validate_and_query.py
```

## To make this real

- Load the same documents into **Azure Cosmos DB** (has a free tier) or **MongoDB Atlas**
  (free tier), and run equivalent queries there instead of SQLite's JSON1 — that's the
  genuinely "nonrelational database" version of this exercise.
- Add a document with a field that violates the schema (e.g. `aflatoxin_ppb: -5` or a
  missing required field) and confirm validation actually rejects it — don't just take the
  happy path's word for it.

## How to describe this on your CV

> Designed a JSON schema for semi-structured research data with variable per-record fields,
> and built validation and query logic against it. [GitHub link]
