# API Design & Security

## What's here

A small, real REST API (`app/main.py`) in front of the aflatoxin readings, plus a test suite
(`app/test_main.py`) that proves the security rules actually hold.

Design decisions worth being able to explain in an interview:
- **Reads are public, writes need an API key** — a deliberate choice, not an oversight
- **Input validation happens before your code runs** (Pydantic rejects a negative ppb value
  with a 422 automatically)
- **Resource-based routes** (`/readings`, `/readings/{id}`) rather than one do-everything endpoint
- **Pagination** on the list endpoint so it doesn't break once there's real data volume
- **Correct status codes** — 201 on create, 404 on missing, 401 on bad auth, 409 on duplicate

## Run it

```
pip install -r requirements.txt
cd app
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000/docs for interactive docs, or run the test suite:
```
python -m pytest test_main.py -v
```

## Taking it further (optional)

- Swap the hardcoded `API_KEY` for an environment variable, then for Azure Key Vault if
  you deploy this to Azure — that's the realistic production version of "never hardcode secrets."
- Deploy it as an Azure App Service or Azure Container App, so you have a live URL to
  demo instead of just localhost.
