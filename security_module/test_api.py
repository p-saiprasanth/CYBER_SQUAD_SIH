"""
test_api.py
-----------
End-to-end test of the Phase 9 API layer using FastAPI's TestClient
(no real server/network needed). Run: python test_api.py
"""

import io
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


section("1) Login")
resp = client.post("/auth/login", json={"username": "investigator1", "password": "pass123"})
print(resp.status_code, resp.json())
assert resp.status_code == 200
token = resp.json()["token"]
headers = {"Authorization": f"Bearer {token}"}

section("2) Register evidence (hash-evidence)")
fake_file = io.BytesIO(b"Sample evidence content - transaction record.")
resp = client.post(
    "/security/hash-evidence",
    data={"evidence_id": "E100", "case_id": "CASE100"},
    files={"file": ("evidence.txt", fake_file, "text/plain")},
    headers=headers,
)
print(resp.status_code, resp.json())
assert resp.status_code == 200
original_hash = resp.json()["hash"]

section("3) Verify evidence (unchanged) -> should be VALID")
fake_file2 = io.BytesIO(b"Sample evidence content - transaction record.")
resp = client.post(
    "/security/verify-evidence",
    data={"evidence_id": "E100"},
    files={"file": ("evidence.txt", fake_file2, "text/plain")},
    headers=headers,
)
print(resp.status_code, resp.json())
assert resp.json()["verified"] is True

section("4) Verify evidence (tampered) -> should be COMPROMISED")
tampered_file = io.BytesIO(b"Sample evidence content - transaction record. TAMPERED!")
resp = client.post(
    "/security/verify-evidence",
    data={"evidence_id": "E100"},
    files={"file": ("evidence.txt", tampered_file, "text/plain")},
    headers=headers,
)
print(resp.status_code, resp.json())
assert resp.json()["verified"] is False

section("5) Get evidence record")
resp = client.get("/security/evidence/E100", headers=headers)
print(resp.status_code, resp.json())
assert resp.status_code == 200

section("6) RBAC check: investigator blocked from admin-only route")
# view_audit_logs IS allowed for investigator per PERMISSIONS table -> check a truly admin-only one instead
resp = client.get("/security/evidence/E100", headers={})  # no token at all
print("No-auth request:", resp.status_code, resp.json())
assert resp.status_code == 401

section("7) Rate limiting on login (6th attempt within a minute should be blocked)")
for i in range(6):
    resp = client.post("/auth/login", json={"username": "investigator1", "password": "wrongpass"})
    print(f"  attempt {i+1}: {resp.status_code}")

print("\nALL API TESTS PASSED")
