"""
blockchain.py
-------------
Phase 4 — Blockchain / Ledger Abstraction.

IMPORTANT: this is a MOCK / STUB ledger for the hackathon MVP.
It stores hash + metadata records in-memory, simulating what a real
permissioned ledger (Hyperledger Fabric or similar) would do.

We NEVER put raw evidence here — only hash + metadata, per the rule:

    Raw Evidence -> SHA-256 hash -> Ledger -> hash + metadata + timestamp -> Verification

The function signatures below (register_evidence, verify_evidence,
get_evidence_record) are the stable interface the rest of the team builds
against. Swapping this in-memory dict for a real Hyperledger Fabric SDK
call later should NOT require changing any calling code.
"""

import secrets
from datetime import datetime, timezone

from security.hashing import hash_evidence
from security.audit import log_action

# --- MOCK LEDGER STORAGE -----------------------------------------------
# Replace this dict with real Hyperledger Fabric chaincode calls later.
_ledger: dict = {}


def register_evidence(evidence_id: str, case_id: str, file_path: str,
                       user_id: str = "SYSTEM") -> dict:
    """
    Hash a piece of evidence and record it on the ledger (mocked).

    Parameters
    ----------
    evidence_id : str   e.g. "E001"
    case_id     : str   e.g. "CASE001"
    file_path   : str   path to the evidence file
    user_id     : str   who registered this evidence

    Returns
    -------
    dict
        The ledger record, including a mock transaction id.
    """
    evidence_hash = hash_evidence(file_path)

    record = {
        "evidence_id": evidence_id,
        "case_id": case_id,
        "hash": evidence_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "EVIDENCE_REGISTERED",
        "tx_id": secrets.token_hex(16),  # stand-in for a real ledger transaction id
    }

    _ledger[evidence_id] = record
    log_action(user_id, "EVIDENCE_ADDED", case_id=case_id, evidence_id=evidence_id)
    return record


def verify_evidence(evidence_id: str, file_path: str, user_id: str = "SYSTEM") -> dict:
    """
    Re-hash a file and compare it against the hash recorded on the ledger.

    Returns
    -------
    dict
        {
          "verified": True/False,
          "message": "✓ Evidence verified" | "⚠ Evidence integrity compromised",
          "current_hash": ...,
          "ledger_hash": ...
        }
    """
    record = _ledger.get(evidence_id)
    if not record:
        return {"verified": False, "message": f"No ledger record found for {evidence_id}"}

    current_hash = hash_evidence(file_path)
    verified = current_hash == record["hash"]

    log_action(
        user_id,
        "EVIDENCE_VERIFIED" if verified else "EVIDENCE_HASH_MISMATCH",
        case_id=record["case_id"],
        evidence_id=evidence_id,
        result="VALID" if verified else "MISMATCH",
    )

    return {
        "verified": verified,
        "message": "✓ Evidence verified" if verified else "⚠ Evidence integrity compromised",
        "current_hash": current_hash,
        "ledger_hash": record["hash"],
    }


def get_evidence_record(evidence_id: str) -> dict:
    """Fetch the ledger record for a piece of evidence, if it exists."""
    return _ledger.get(evidence_id)


if __name__ == "__main__":
    import tempfile, os

    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp:
        tmp.write("Original crime-scene evidence content.")
        path = tmp.name

    print("1) Register evidence")
    record = register_evidence("E001", "CASE001", path, user_id="U001")
    print("  ", record)

    print("\n2) Verify (unchanged) -> should be VALID")
    result = verify_evidence("E001", path, user_id="U001")
    print("  ", result["message"])

    print("\n3) Tamper with the evidence file")
    with open(path, "a") as f:
        f.write(" ...someone modified this.")

    print("\n4) Verify again -> should be TAMPERING DETECTED")
    result = verify_evidence("E001", path, user_id="U001")
    print("  ", result["message"])

    os.remove(path)
