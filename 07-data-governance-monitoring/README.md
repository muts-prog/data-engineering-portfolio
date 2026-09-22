# 07 — Data Governance & Monitoring

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
