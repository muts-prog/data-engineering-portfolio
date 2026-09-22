# 04 — DevOps Basics (CI/CD)

**JD line this targets:** "Familiarity with basic DevOps is a plus."

## What's here

`.github/workflows/ci.yml` — a GitHub Actions workflow that automatically, on every push:
1. installs dependencies
2. lints the code (`ruff`)
3. runs the API tests from folder 03
4. runs the pipeline tests (`tests/test_pipeline.py`), which actually execute folder 01's
   ingestion script and check the output data quality

This is "basic DevOps" in its most honest form — not Kubernetes or infrastructure-as-code,
but the habit of automatically catching a broken pipeline or API before it reaches anyone.

## To make this real

Once this whole `gap-portfolio` folder is pushed to a real GitHub repo, the workflow in
`.github/workflows/ci.yml` needs to live at the **repo root** under `.github/workflows/` (GitHub
only looks there) — so when you push, copy that file up, adjusting the working-directory
paths to match wherever you place the other folders.

Push a small breaking change on purpose once (e.g. make a test fail) and watch the Actions
tab turn red — that's worth being able to describe in an interview: "I've seen CI actually
catch something."

## How to describe this on your CV

> Set up a GitHub Actions CI pipeline to automatically lint and test a data pipeline and API
> on every push. [GitHub link]
