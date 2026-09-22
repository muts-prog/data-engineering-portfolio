"""
Builds the star schema in SQLite, loads it from the clean CSV produced in folder 01,
and runs a couple of analytical queries against it — proving the model actually
supports the questions a stakeholder would ask.

Run:
    python load_and_query.py
"""
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "warehouse.db"
CLEAN_CSV = "../../01-fabric-lakehouse-pipeline/data/aflatoxin_clean.csv"
SCHEMA_SQL = "schema_dimensional_model.sql"

Path(DB_PATH).unlink(missing_ok=True)
conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_SQL) as f:
    conn.executescript(f.read())

df = pd.read_csv(CLEAN_CSV, parse_dates=["collection_date"])

# --- Build dimensions from the source data ---
counties = pd.DataFrame({"county_name": sorted(df["county"].unique())})
counties["county_key"] = counties.index + 1
counties.to_sql("dim_county", conn, if_exists="append", index=False)

crops = pd.DataFrame({"crop_name": sorted(df["crop"].unique())})
crops["crop_key"] = crops.index + 1
crops.to_sql("dim_crop", conn, if_exists="append", index=False)

labs = pd.DataFrame({"lab_id": sorted(df["lab_id"].unique())})
labs["lab_key"] = labs.index + 1
labs.to_sql("dim_lab", conn, if_exists="append", index=False)

dates = pd.DataFrame({"full_date": sorted(df["collection_date"].dt.strftime("%Y-%m-%d").unique())})
dates["date_key"] = dates["full_date"].str.replace("-", "").astype(int)
dates["year"] = pd.to_datetime(dates["full_date"]).dt.year
dates["month"] = pd.to_datetime(dates["full_date"]).dt.month
dates["day"] = pd.to_datetime(dates["full_date"]).dt.day
dates["week_of_year"] = pd.to_datetime(dates["full_date"]).dt.isocalendar().week
dates.to_sql("dim_date", conn, if_exists="append", index=False)

# --- Build the fact table by joining source data to the surrogate keys ---
fact = df.copy()
fact["date_key"] = fact["collection_date"].dt.strftime("%Y%m%d").astype(int)
fact = fact.merge(counties, left_on="county", right_on="county_name")
fact = fact.merge(crops, left_on="crop", right_on="crop_name")
fact = fact.merge(labs, left_on="lab_id", right_on="lab_id")
fact["reading_key"] = fact.index + 1
fact["exceeds_10ppb"] = fact["exceeds_10ppb"].astype(int)

fact_final = fact[["reading_key", "sample_id", "county_key", "crop_key", "lab_key",
                    "date_key", "soil_moisture_pct", "temperature_c", "aflatoxin_ppb",
                    "exceeds_10ppb"]]
fact_final.to_sql("fact_aflatoxin_reading", conn, if_exists="append", index=False)

print(f"Loaded {len(fact_final)} fact rows.\n")

# --- Analytical queries a stakeholder would actually ask for ---
print("Top 3 counties by share of readings exceeding 10ppb:")
q1 = """
SELECT c.county_name,
       ROUND(AVG(f.exceeds_10ppb) * 100, 1) AS pct_exceeding,
       COUNT(*) AS n_samples
FROM fact_aflatoxin_reading f
JOIN dim_county c ON f.county_key = c.county_key
GROUP BY c.county_name
ORDER BY pct_exceeding DESC
LIMIT 3;
"""
print(pd.read_sql(q1, conn), "\n")

print("Monthly trend of average aflatoxin level:")
q2 = """
SELECT d.year, d.month, ROUND(AVG(f.aflatoxin_ppb), 2) AS avg_ppb
FROM fact_aflatoxin_reading f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
"""
print(pd.read_sql(q2, conn))

conn.close()
