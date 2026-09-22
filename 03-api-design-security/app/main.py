"""
A small, real API in front of the aflatoxin readings — built to demonstrate API design
and security fundamentals, not just "consuming a JSON API" (which the CV already covers).

Run:
    uvicorn main:app --reload
Then visit http://127.0.0.1:8000/docs for interactive API docs (auto-generated).

Demonstrates:
- Resource-based routing (REST conventions, not just one big endpoint)
- Request/response validation via Pydantic models (bad input gets rejected with a 422,
  not silently accepted)
- API key authentication (a header-based key, checked on every write)
- Sensible status codes (201 on create, 404 on missing, 401 on bad auth)
- Pagination on the list endpoint, so it doesn't fall over once there's real volume
"""
import csv
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Aflatoxin Readings API", version="1.0")

DATA_PATH = Path(__file__).parent.parent / "data" / "readings.csv"
API_KEY = "demo-key-change-me"  # in real use: env var / Azure Key Vault, never hardcoded


def load_readings():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH) as f:
        return list(csv.DictReader(f))


def save_readings(rows):
    DATA_PATH.parent.mkdir(exist_ok=True)
    with open(DATA_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["sample_id", "county", "crop", "aflatoxin_ppb"])
        writer.writeheader()
        writer.writerows(rows)


class ReadingIn(BaseModel):
    sample_id: str = Field(..., min_length=1)
    county: str
    crop: str
    aflatoxin_ppb: float = Field(..., ge=0, description="Must be zero or positive")


class ReadingOut(ReadingIn):
    pass


def check_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


@app.get("/readings", response_model=list[ReadingOut])
def list_readings(limit: int = Query(20, le=100), offset: int = Query(0, ge=0)):
    """Public, read-only, paginated — no key needed to read published data."""
    rows = load_readings()
    return rows[offset: offset + limit]


@app.get("/readings/{sample_id}", response_model=ReadingOut)
def get_reading(sample_id: str):
    rows = load_readings()
    for r in rows:
        if r["sample_id"] == sample_id:
            return r
    raise HTTPException(status_code=404, detail=f"No reading found for {sample_id}")


@app.post("/readings", response_model=ReadingOut, status_code=201)
def create_reading(reading: ReadingIn, x_api_key: str | None = Header(None)):
    """Writes require an API key — reads don't. This split is a deliberate security decision."""
    check_api_key(x_api_key)
    rows = load_readings()
    if any(r["sample_id"] == reading.sample_id for r in rows):
        raise HTTPException(status_code=409, detail="sample_id already exists")
    rows.append(reading.model_dump())
    save_readings(rows)
    return reading


@app.delete("/readings/{sample_id}", status_code=204)
def delete_reading(sample_id: str, x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    rows = load_readings()
    new_rows = [r for r in rows if r["sample_id"] != sample_id]
    if len(new_rows) == len(rows):
        raise HTTPException(status_code=404, detail=f"No reading found for {sample_id}")
    save_readings(new_rows)
