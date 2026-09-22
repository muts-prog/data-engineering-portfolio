# 08 — ERP / CRM Integration

## What's here

- `scripts/mock_crm_server.py` — a tiny stand-in for a real CRM's REST API (deliberately
  shaped like Espo CRM's `/Contact` endpoint), just enough to demonstrate the integration
  pattern without needing a real Espo/NRC Collect instance.
- `scripts/crm_client.py` — a client that authenticates with an API key, reads existing
  contacts, creates a new one, and confirms it landed — a full read/write round trip, with
  proper error handling if the server isn't reachable.

Run (two terminals, or one shell session backgrounding the server):
```
python scripts/mock_crm_server.py
# in another terminal:
python scripts/crm_client.py
```
