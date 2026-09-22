# 01 — Fabric Lakehouse Pipeline

**JD line this targets:** "Build data pipelines in Fabric to integrate internal and external
data based on existing internal best practices."

## What's here

- `data/raw_aflatoxin_samples.csv` — a synthetic dataset shaped like real field-collected
  aflatoxin data, deliberately messy (nulls, inconsistent casing) so the cleaning step means
  something.
- `notebooks/ingest_transform.py` — ingests it, cleans it, adds a derived column, runs data
  quality checks, and writes a clean output. Runs as-is with `python ingest_transform.py`.

## To make this real in Fabric (not just local pandas)

1. In your Fabric workspace, create a **Lakehouse**.
2. Upload `raw_aflatoxin_samples.csv` to `Files/raw/`.
3. Create a **Notebook** attached to the Lakehouse and port the logic over, swapping the
   pandas calls for the PySpark equivalents noted in the script's comments.
4. Write the result as a managed Delta table (`saveAsTable`) instead of a CSV — that's the bit
   that actually demonstrates "Lakehouse," not just "wrote a Python script."
5. Optional: wrap the notebook in a **Fabric Data Pipeline** with a schedule, so it's a
   pipeline and not just a one-off notebook run.

## How to describe this on your CV, once you've done step 2–5 for real

> Built a data ingestion and transformation pipeline in Microsoft Fabric (Lakehouse, Delta
> tables) to clean and structure field-collected research data, including automated data
> quality checks. [GitHub link]

Don't claim the Fabric part until you've actually run it in the Fabric portal — the local
pandas version is the design, not the deliverable.
