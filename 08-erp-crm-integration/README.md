# 08 — ERP / CRM Integration

**JD line this targets:** "Integrations with NRC Collect or Espo CRM and other systems"
and "familiarity in working with enterprise information systems in general, and especially
ERP and CRM."

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

## Why a mock server, not a note saying "would integrate with Espo CRM"

Because the point isn't Espo CRM specifically — it's proving you can read API docs, handle
auth headers, parse JSON responses, and deal with connection failures gracefully. Swapping
`BASE_URL` and the auth header in `crm_client.py` is genuinely most of the work of pointing
this at a real Espo CRM or NRC Collect instance later.

## To make this real

- If you can get a free/trial Espo CRM instance running (it's open source — self-hostable via
  Docker), point `crm_client.py` at its real REST API and auth scheme instead of the mock.
- Add retry logic with backoff for transient failures — a small addition that signals you're
  thinking about production reliability, not just the happy path.

## How to describe this on your CV

> Built a REST API integration client (auth, read/write, error handling) against a
> CRM-style API, demonstrating the integration pattern used for systems like Espo CRM.
> [GitHub link]

Keep the claim to "the pattern" until you've actually pointed it at a real Espo/CRM system —
that's an honest distinction worth holding onto in an interview.
