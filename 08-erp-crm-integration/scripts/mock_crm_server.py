"""
A tiny stand-in for a system like Espo CRM's REST API — just enough to demonstrate the
INTEGRATION PATTERN (auth header, JSON in/out, pagination, error handling) without needing
an actual Espo CRM instance to spin up. crm_client.py talks to this exact same way it would
talk to a real Espo/CRM/NRC Collect REST API.

Run this first, in its own terminal:
    python mock_crm_server.py
Then in another terminal:
    python crm_client.py
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

CONTACTS = [
    {"id": "1", "name": "Amina Yusuf", "role": "Field Officer", "county": "Turkana"},
    {"id": "2", "name": "Peter Mwangi", "role": "Programme Manager", "county": "Nairobi"},
]
API_KEY = "mock-crm-key"


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _check_auth(self):
        key = self.headers.get("X-Api-Key")
        if key != API_KEY:
            self._send_json(401, {"error": "invalid or missing API key"})
            return False
        return True

    def do_GET(self):
        if not self._check_auth():
            return
        if self.path == "/Contact":
            self._send_json(200, {"list": CONTACTS, "total": len(CONTACTS)})
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        if not self._check_auth():
            return
        if self.path == "/Contact":
            length = int(self.headers.get("Content-Length", 0))
            new_contact = json.loads(self.rfile.read(length))
            new_contact["id"] = str(len(CONTACTS) + 1)
            CONTACTS.append(new_contact)
            self._send_json(201, new_contact)
        else:
            self._send_json(404, {"error": "not found"})

    def log_message(self, format, *args):
        pass  # keep the demo output quiet; remove this to see request logs


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8800), Handler)
    print("Mock CRM running on http://127.0.0.1:8800 (Ctrl+C to stop)")
    server.serve_forever()
