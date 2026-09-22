"""
Ingest + transform: raw aflatoxin field samples -> clean Lakehouse table.

Written in pandas so it runs anywhere while you're building it locally. Notes throughout
show the direct equivalent in a real Fabric notebook (which runs PySpark against a Lakehouse).

Run locally:
    python ingest_transform.py

In Fabric:
    1. Create a Lakehouse in your workspace.
    2. Upload data/raw_aflatoxin_samples.csv to Files/raw/.
    3. Paste this logic into a new Notebook attached to that Lakehouse, swapping the
       pandas calls for the PySpark equivalents noted in the comments.
    4. Write the result with df.write.format("delta").saveAsTable("aflatoxin_clean")
       instead of to_csv — that's what actually lands it in the Lakehouse as a managed table.
"""
import pandas as pd

RAW_PATH = "../data/raw_aflatoxin_samples.csv"
OUT_PATH = "../data/aflatoxin_clean.csv"

# --- Ingest -----------------------------------------------------------------
# Fabric equivalent: df = spark.read.format("csv").option("header", True).load("Files/raw/...")
df = pd.read_csv(RAW_PATH)
raw_row_count = len(df)

# --- Clean & standardize -----------------------------------------------------
# Fabric equivalent: df.withColumn("county", F.initcap(F.col("county")))
df["county"] = df["county"].str.strip().str.title()

# Fabric equivalent: df.fillna({"temperature_c": df.select(F.mean("temperature_c")).first()[0]})
df["temperature_c"] = df["temperature_c"].fillna(df["temperature_c"].mean().round(1))

df["collection_date"] = pd.to_datetime(df["collection_date"])

# --- Derive a risk flag (business logic lives in the pipeline, not just the report) ----
# WHO/EU indicative threshold for aflatoxin in maize is commonly cited around 10 ppb;
# used here only to demonstrate a transformation rule, not as regulatory guidance.
df["exceeds_10ppb"] = df["aflatoxin_ppb"] > 10

# --- Data quality checks before we "load" ------------------------------------
assert df["sample_id"].is_unique, "Duplicate sample_id found — would break the Lakehouse table's grain"
assert df["aflatoxin_ppb"].ge(0).all(), "Negative aflatoxin reading — upstream sensor/entry error"
assert df["temperature_c"].isna().sum() == 0, "Nulls remain after fill — investigate before loading"

# --- Load ---------------------------------------------------------------------
# Fabric equivalent: df.write.format("delta").mode("overwrite").saveAsTable("aflatoxin_clean")
df.to_csv(OUT_PATH, index=False)

print(f"Ingested {raw_row_count} raw rows -> wrote {len(df)} clean rows to {OUT_PATH}")
print(df.groupby("county")["exceeds_10ppb"].mean().round(2).sort_values(ascending=False))
