"""
Runs the ingestion/transformation pipeline from folder 01 and checks its output meets
the data quality bar — this is what CI is actually for: catching a broken pipeline
automatically, on every push, instead of a human noticing bad data downstream.
"""
import subprocess
import sys
from pathlib import Path
import pandas as pd

PIPELINE_DIR = Path(__file__).parent.parent.parent / "01-fabric-lakehouse-pipeline" / "notebooks"
OUTPUT_CSV = PIPELINE_DIR.parent / "data" / "aflatoxin_clean.csv"


def test_pipeline_runs_successfully():
    result = subprocess.run(
        [sys.executable, "ingest_transform.py"],
        cwd=PIPELINE_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Pipeline failed:\n{result.stderr}"


def test_output_has_no_nulls_in_key_columns():
    df = pd.read_csv(OUTPUT_CSV)
    assert df["temperature_c"].isna().sum() == 0
    assert df["aflatoxin_ppb"].isna().sum() == 0


def test_output_has_unique_sample_ids():
    df = pd.read_csv(OUTPUT_CSV)
    assert df["sample_id"].is_unique


def test_no_negative_readings():
    df = pd.read_csv(OUTPUT_CSV)
    assert (df["aflatoxin_ppb"] >= 0).all()
