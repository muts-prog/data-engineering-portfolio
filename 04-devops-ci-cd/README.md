# 04 — DevOps Basics (CI/CD)

## What's here

`.github/workflows/ci.yml` — a GitHub Actions workflow that automatically, on every push:
1. installs dependencies
2. lints the code (`ruff`)
3. runs the API tests from folder 03
4. runs the pipeline tests (`tests/test_pipeline.py`), which actually execute folder 01's
   ingestion script and check the output data quality

This is "basic DevOps" in its most honest form — not Kubernetes or infrastructure-as-code,
but the habit of automatically catching a broken pipeline or API before it reaches anyone.
