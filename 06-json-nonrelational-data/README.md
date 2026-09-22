# 06 — JSON / Non-Relational Data

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
