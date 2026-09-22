"""
A standalone data quality report — the kind of check that, in production, would run as a
scheduled Fabric pipeline step or Azure Function before data is trusted downstream, and
would alert someone (email, Teams webhook, etc.) if a check fails.

Run:
    python data_quality_report.py
Exit code is non-zero if any HARD check fails — that's what makes this usable in CI
(see folder 04) or as a pipeline gate, not just a report a human reads after the fact.
"""
import sys
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "raw_aflatoxin_samples.csv"

EXPECTED_COLUMNS = {
    "sample_id", "county", "crop", "collection_date",
    "soil_moisture_pct", "temperature_c", "aflatoxin_ppb", "lab_id",
}
VALID_COUNTIES = {"Nairobi", "Kiambu", "Machakos", "Nakuru", "Meru", "Kisumu", "Bungoma"}


class Check:
    def __init__(self, name, passed, detail, severity="hard"):
        self.name = name
        self.passed = passed
        self.detail = detail
        self.severity = severity  # "hard" fails the run; "soft" just warns


def run_checks(df: pd.DataFrame) -> list[Check]:
    checks = []

    # Schema check — catches an upstream source silently changing its export format
    missing_cols = EXPECTED_COLUMNS - set(df.columns)
    checks.append(Check(
        "expected_columns_present", len(missing_cols) == 0,
        f"Missing columns: {missing_cols}" if missing_cols else "All expected columns present",
    ))

    # Completeness
    null_counts = df.isna().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    checks.append(Check(
        "no_unexpected_nulls", cols_with_nulls.empty,
        f"Nulls found in: {dict(cols_with_nulls)}" if not cols_with_nulls.empty else "No nulls",
        severity="soft",  # some nulls (like temperature_c here) are expected and get fixed downstream
    ))

    # Uniqueness — this one is a hard fail: a duplicate sample_id breaks every downstream join
    dupes = df["sample_id"].duplicated().sum()
    checks.append(Check(
        "unique_sample_ids", dupes == 0, f"{dupes} duplicate sample_id(s) found",
    ))

    # Range check — a negative reading means a sensor or entry error, not a real value
    bad_range = (df["aflatoxin_ppb"] < 0).sum()
    checks.append(Check(
        "aflatoxin_ppb_non_negative", bad_range == 0, f"{bad_range} negative reading(s) found",
    ))

    # Referential/categorical check — catches typos or unexpected new categories silently entering
    bad_counties = set(df["county"].str.strip().unique()) - VALID_COUNTIES
    checks.append(Check(
        "counties_in_known_list", len(bad_counties) == 0,
        f"Unrecognized counties: {bad_counties}" if bad_counties else "All counties recognized",
        severity="soft",  # could be a legitimate new county, worth a warning rather than blocking
    ))

    # Freshness — a real pipeline would check "was new data actually collected today?"
    latest_date = pd.to_datetime(df["collection_date"]).max()
    days_old = (pd.Timestamp.now() - latest_date).days
    checks.append(Check(
        "data_not_stale", days_old < 400,  # generous threshold since this is a static demo dataset
        f"Latest record is {days_old} days old",
        severity="soft",
    ))

    return checks


def main():
    df = pd.read_csv(DATA_PATH)
    checks = run_checks(df)

    print(f"Data quality report for {DATA_PATH.name} — {len(df)} rows\n")
    hard_failures = 0
    for c in checks:
        status = "PASS" if c.passed else ("FAIL" if c.severity == "hard" else "WARN")
        print(f"  [{status:4}] {c.name}: {c.detail}")
        if not c.passed and c.severity == "hard":
            hard_failures += 1

    print(f"\n{hard_failures} hard failure(s).")
    # Non-zero exit code is what lets a CI pipeline or Fabric pipeline treat this as a gate,
    # not just a report nobody reads.
    sys.exit(1 if hard_failures > 0 else 0)


if __name__ == "__main__":
    main()
