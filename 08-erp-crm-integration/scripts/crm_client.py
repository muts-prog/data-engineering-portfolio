"""
Integration client — talks to the mock CRM (or a real Espo CRM / NRC Collect instance,
by changing BASE_URL and the auth header) to pull field-officer contacts and push a new one.

Requires mock_crm_server.py to be running first (python mock_crm_server.py).

Run:
    python crm_client.py
"""
import requests
import sys

BASE_URL = "http://127.0.0.1:8800"
API_KEY = "mock-crm-key"
HEADERS = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}


def get_contacts():
    resp = requests.get(f"{BASE_URL}/Contact", headers=HEADERS, timeout=5)
    resp.raise_for_status()  # fail loudly and clearly on a bad response, not silently
    return resp.json()


def create_contact(name: str, role: str, county: str):
    payload = {"name": name, "role": role, "county": county}
    resp = requests.post(f"{BASE_URL}/Contact", headers=HEADERS, json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()


def main():
    try:
        data = get_contacts()
    except requests.exceptions.ConnectionError:
        print("Couldn't reach the mock CRM — start it first with: python mock_crm_server.py")
        sys.exit(1)

    print(f"Existing contacts ({data['total']}):")
    for c in data["list"]:
        print(f"  {c['id']}: {c['name']} — {c['role']}, {c['county']}")

    new = create_contact("Grace Wanjiru", "Data Officer", "Kisumu")
    print(f"\nCreated contact: {new}")

    data_after = get_contacts()
    print(f"\nTotal contacts now: {data_after['total']}")


if __name__ == "__main__":
    main()
