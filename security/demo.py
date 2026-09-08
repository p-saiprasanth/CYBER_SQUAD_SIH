"""
demo.py
-------
Phase 8 — Demo script.

Run this to show judges the full evidence-integrity flow end-to-end:

1. Register evidence (hash + store on the ledger)
2. Verify evidence -> VALID
3. Tamper with the evidence
4. Verify again -> TAMPERING DETECTED
5. Show the audit trail that recorded every step

Also demonstrates RBAC: an investigator can upload evidence, but is
blocked from an admin-only action.
"""

import os
import tempfile

from security.blockchain import register_evidence, verify_evidence, get_evidence_record
from security.audit import get_audit_trail
from security.auth import register_user, authenticate_user, require_permission, PermissionDenied


def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    # ---- Set up demo users ----
    register_user("U001", "investigator1", "pass123", "INVESTIGATOR")
    register_user("U002", "admin1", "adminpass", "ADMIN")

    section("STEP 0 — Login")
    login = authenticate_user("investigator1", "pass123")
    print(f"Investigator1 logged in. Role: {login['role']}")
    token = login["token"]

    # ---- Create a sample evidence file ----
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp:
        tmp.write("CASE001 - Suspect financial transaction record - original content.")
        evidence_path = tmp.name

    section("STEP 1 — Register evidence")
    record = register_evidence("E001", "CASE001", evidence_path, user_id="U001")
    print(f"Evidence registered.\n  evidence_id: {record['evidence_id']}")
    print(f"  hash:        {record['hash']}")
    print(f"  tx_id:       {record['tx_id']}")

    section("STEP 2 — Verify evidence (unchanged)")
    result = verify_evidence("E001", evidence_path, user_id="U001")
    print(result["message"])
    assert result["verified"] is True

    section("STEP 3 — Tamper with the evidence file")
    with open(evidence_path, "a") as f:
        f.write(" [TAMPERED: amount changed from $500 to $50,000]")
    print("File modified on disk.")

    section("STEP 4 — Verify evidence again (should detect tampering)")
    result = verify_evidence("E001", evidence_path, user_id="U001")
    print(result["message"])
    assert result["verified"] is False

    section("STEP 5 — Audit trail for CASE001")
    for event in get_audit_trail(case_id="CASE001"):
        print(f"  [{event['timestamp']}] {event['action']} by {event['user_id']} "
              f"(evidence={event['evidence_id']}, result={event['result']})")

    section("STEP 6 — RBAC check: investigator blocked from admin action")

    @require_permission("manage_users")
    def manage_users(token):
        return "User management panel opened."

    try:
        manage_users(token)
        print("ERROR: investigator was NOT blocked (this should not happen)")
    except PermissionDenied as e:
        print(f"Blocked as expected: {e}")

    os.remove(evidence_path)
    section("DEMO COMPLETE")


if __name__ == "__main__":
    main()
