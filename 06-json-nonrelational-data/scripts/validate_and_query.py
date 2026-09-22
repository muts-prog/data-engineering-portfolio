"""
Two things a JSON-document workflow needs that a flat CSV doesn't:
1. Schema validation — documents can vary in shape, but not arbitrarily; jsonschema
   catches a malformed document before it's stored.
2. Querying into nested structure — SQLite's JSON1 extension lets you query nested
   fields with plain SQL, which is close to how Cosmos DB / MongoDB queries feel,
   without needing either installed to demonstrate the idea.

Run:
    python validate_and_query.py
"""
import json
import sqlite3
from pathlib import Path
from jsonschema import validate, ValidationError

SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "reading_document_schema.json"
DOCS_PATH = Path(__file__).parent.parent / "schema" / "sample_documents.json"

schema = json.loads(SCHEMA_PATH.read_text())
documents = json.loads(DOCS_PATH.read_text())

# --- 1. Validate every document against the schema ---------------------------
print("Validating documents against schema...")
for doc in documents:
    try:
        validate(instance=doc, schema=schema)
        print(f"  OK   {doc['sample_id']}")
    except ValidationError as e:
        print(f"  FAIL {doc['sample_id']}: {e.message}")

# --- 2. Load into SQLite as JSON and query into nested fields ----------------
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE readings_json (sample_id TEXT PRIMARY KEY, doc JSON)")
for d in documents:
    conn.execute(
        "INSERT INTO readings_json VALUES (?, ?)",
        (d["sample_id"], json.dumps(d)),
    )
conn.commit()

print("\nQuerying into nested metadata with plain SQL (SQLite JSON1):")
query = """
SELECT
    sample_id,
    json_extract(doc, '$.county') AS county,
    json_extract(doc, '$.metadata.collection_method') AS collection_method,
    json_extract(doc, '$.metadata.gps.lat') AS lat,
    json_extract(doc, '$.metadata.flagged_for_review') AS flagged
FROM readings_json;
"""
for row in conn.execute(query):
    print(" ", row)

print("\nDocuments missing GPS data entirely (shows why a fixed schema would force a NULL column):")
for row in conn.execute(
    "SELECT sample_id FROM readings_json WHERE json_extract(doc, '$.metadata.gps') IS NULL"
):
    print(" ", row[0])

conn.close()
