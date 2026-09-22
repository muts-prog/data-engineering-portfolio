-- Star-schema warehouse design for the aflatoxin monitoring data.
-- Written in standard SQL (tested against SQLite locally); works unchanged against
-- a Fabric Warehouse or Azure SQL / PostgreSQL with minor type tweaks noted inline.

-- ============ DIMENSION TABLES ============

CREATE TABLE dim_county (
    county_key      INTEGER PRIMARY KEY,   -- Fabric/Azure SQL: use IDENTITY(1,1) instead
    county_name     TEXT NOT NULL UNIQUE,
    region          TEXT
);

CREATE TABLE dim_crop (
    crop_key        INTEGER PRIMARY KEY,
    crop_name       TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_lab (
    lab_key         INTEGER PRIMARY KEY,
    lab_id          TEXT NOT NULL UNIQUE,
    lab_name        TEXT
);

CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,   -- surrogate key, e.g. 20260315
    full_date       TEXT NOT NULL,
    year            INTEGER NOT NULL,
    month           INTEGER NOT NULL,
    day             INTEGER NOT NULL,
    week_of_year    INTEGER NOT NULL
);

-- ============ FACT TABLE ============

CREATE TABLE fact_aflatoxin_reading (
    reading_key     INTEGER PRIMARY KEY,
    sample_id       TEXT NOT NULL UNIQUE,   -- natural key, kept for traceability back to source
    county_key      INTEGER NOT NULL REFERENCES dim_county(county_key),
    crop_key        INTEGER NOT NULL REFERENCES dim_crop(crop_key),
    lab_key         INTEGER NOT NULL REFERENCES dim_lab(lab_key),
    date_key        INTEGER NOT NULL REFERENCES dim_date(date_key),
    soil_moisture_pct  REAL,
    temperature_c      REAL,
    aflatoxin_ppb       REAL NOT NULL,
    exceeds_10ppb       INTEGER NOT NULL   -- 0/1, kept from the transform step as a measure
);

-- Indexes that matter once this table has real volume — Fabric Warehouse and most
-- cloud warehouses handle this differently (clustered columnstore is often the default),
-- but the *intent* — fast filtering on the columns analysts actually query by — is the same.
CREATE INDEX idx_fact_county ON fact_aflatoxin_reading(county_key);
CREATE INDEX idx_fact_date   ON fact_aflatoxin_reading(date_key);
