from fastapi.testclient import TestClient
from main import API_KEY, app

client = TestClient(app)


def test_create_requires_api_key():
    resp = client.post("/readings", json={
        "sample_id": "TEST1", "county": "Nairobi", "crop": "Maize", "aflatoxin_ppb": 3.2
    })
    assert resp.status_code == 401


def test_create_with_key_succeeds():
    resp = client.post(
        "/readings",
        json={"sample_id": "TEST2", "county": "Nairobi", "crop": "Maize", "aflatoxin_ppb": 3.2},
        headers={"x-api-key": API_KEY},
    )
    assert resp.status_code == 201


def test_negative_ppb_rejected():
    resp = client.post(
        "/readings",
        json={"sample_id": "TEST3", "county": "Nairobi", "crop": "Maize", "aflatoxin_ppb": -1},
        headers={"x-api-key": API_KEY},
    )
    assert resp.status_code == 422  # Pydantic validation catches it before our code even runs


def test_get_missing_sample_returns_404():
    resp = client.get("/readings/DOES-NOT-EXIST")
    assert resp.status_code == 404


def test_list_is_paginated():
    resp = client.get("/readings?limit=1")
    assert resp.status_code == 200
    assert len(resp.json()) <= 1
