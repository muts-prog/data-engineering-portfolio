"""
Applies every migration in migrations/ in order, against a fresh SQLite database,
inserting a couple of rows partway through to prove the "safe column addition" pattern
actually works against data that already exists — not just an empty table.

Run:
    python run_migrations.py
"""
import sqlite3
from pathlib import Path

DB_PATH = "readings.db"
MIGRATIONS_DIR = Path("migrations")

Path(DB_PATH).unlink(missing_ok=True)
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")

migrations = sorted(MIGRATIONS_DIR.glob("*.sql"))

for i, migration in enumerate(migrations):
    print(f"Applying {migration.name} ...")
    conn.executescript(migration.read_text())

    # After the very first migration (table exists, empty), insert some rows —
    # this is the moment that proves 0002/0003/0004 are safe against *existing* data,
    # which is the entire point of the three-step pattern.
    if i == 0:
        conn.execute(
            "INSERT INTO readings (sample_id, county, crop, aflatoxin_ppb) VALUES (?, ?, ?, ?)",
            ("PRE-EXISTING-1", "Nairobi", "Maize", 4.5),
        )
        conn.execute(
            "INSERT INTO readings (sample_id, county, crop, aflatoxin_ppb) VALUES (?, ?, ?, ?)",
            ("PRE-EXISTING-2", "Kiambu", "Sorghum", 2.1),
        )
        conn.commit()
        print("  -> inserted 2 rows before the schema evolves further")

conn.commit()

print("\nFinal schema:")
for row in conn.execute("PRAGMA table_info(readings)"):
    print(" ", row)

print("\nFinal data (note: pre-existing rows now have lab_id = 'UNKNOWN', not NULL):")
for row in conn.execute("SELECT sample_id, lab_id FROM readings"):
    print(" ", row)

conn.close()
