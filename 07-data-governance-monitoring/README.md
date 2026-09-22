# 07 — Data Governance & Monitoring

**JD line this targets:** "Proactively implement data validation checks, monitoring and
error-handling processes to ensure the accuracy, consistency, and integrity of data."

## What's here

`scripts/data_quality_report.py` runs six checks against the raw dataset — schema presence,
completeness, uniqueness, valid ranges, known categories, and freshness — and separates them
into **hard failures** (block the pipeline) and **soft warnings** (worth a human's attention,
not worth stopping the run). It exits with a non-zero code on any hard failure, which is what
lets this plug into CI (folder 04) or a pipeline as an actual gate, not just a report nobody
reads.

Run:
```
python scripts/data_quality_report.py
```

## To make this real

- In Fabric: add this as a **notebook activity** early in a Data Pipeline, and set the
  pipeline to stop (or route to an alert) if the notebook exits non-zero.
- Wire a Teams webhook or email step to fire only on hard failures — that's the "monitoring"
  half, not just the "validation" half.
- Consider swapping the hand-rolled checks for a library like **Great Expectations** once you
  want something more standardized — worth mentioning you know it exists even if this version
  is hand-rolled.

## How to describe this on your CV

> Built automated data quality checks (schema, completeness, range, and freshness validation)
> that gate a data pipeline on hard failures while surfacing softer issues as warnings. [GitHub link]
