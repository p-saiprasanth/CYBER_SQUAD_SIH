"""
audit.py
--------
Phase 5 — Audit Logging.

Every important action in the system produces an audit event. This gives
a full accountability trail: who did what, when, from where, and on which
case/evidence. Critical for both security review and legal defensibility.

For the hackathon MVP this stores logs in-memory and mirrors them to a
local JSON file, so logs survive a process restart during the demo.
"""

import json
import os
from datetime import datetime, timezone

LOG_FILE = os.path.join(os.path.dirname(__file__), "audit_log.json")

# Canonical set of actions the system can log. Keep this list in sync
# with what Aman's audit_logs schema expects (Phase 9).
ACTIONS = {
    "LOGIN",
    "CASE_CREATED",
    "EVIDENCE_ADDED",
    "EVIDENCE_UPLOADED",
    "EVIDENCE_PROCESSED",
    "EVIDENCE_VERIFIED",
    "EVIDENCE_HASH_MISMATCH",
    "GRAPH_GENERATED",
    "GRAPH_ACCESSED",
    "AI_QUERY",
    "PREDICTION_GENERATED",
    "REPORT_EXPORTED",
}

_audit_trail: list[dict] = []  # in-memory store for the current process


def log_action(user_id: str, action: str, case_id: str = None,
                evidence_id: str = None, ip: str = None, result: str = None) -> dict:
    """
    Record an audit event.

    Parameters
    ----------
    user_id     : str   who performed the action, e.g. "U001"
    action      : str   must be one of ACTIONS (e.g. "EVIDENCE_VERIFIED")
    case_id     : str   optional, e.g. "CASE001"
    evidence_id : str   optional, e.g. "E001"
    ip          : str   optional, requester IP address
    result      : str   optional, e.g. "VALID" / "MISMATCH"

    Returns
    -------
    dict
        The audit event that was logged.
    """
    if action not in ACTIONS:
        raise ValueError(f"Unknown audit action: {action!r}. Add it to ACTIONS first.")

    event = {
        "user_id": user_id,
        "action": action,
        "case_id": case_id,
        "evidence_id": evidence_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip": ip,
        "result": result,
    }

    _audit_trail.append(event)
    _persist()
    return event


def get_audit_trail(case_id: str = None, evidence_id: str = None) -> list:
    """
    Retrieve logged audit events, optionally filtered by case_id and/or evidence_id.
    """
    events = _audit_trail
    if case_id:
        events = [e for e in events if e.get("case_id") == case_id]
    if evidence_id:
        events = [e for e in events if e.get("evidence_id") == evidence_id]
    return events


def _persist():
    """Mirror the in-memory audit trail to a local JSON file (demo persistence)."""
    with open(LOG_FILE, "w") as f:
        json.dump(_audit_trail, f, indent=2)


if __name__ == "__main__":
    log_action("U001", "LOGIN", ip="10.0.0.5")
    log_action("U001", "CASE_CREATED", case_id="CASE001", ip="10.0.0.5")
    log_action("U001", "EVIDENCE_UPLOADED", case_id="CASE001", evidence_id="E001", ip="10.0.0.5")
    log_action("U001", "EVIDENCE_VERIFIED", case_id="CASE001", evidence_id="E001",
               ip="10.0.0.5", result="VALID")

    print("Audit trail for CASE001:")
    for e in get_audit_trail(case_id="CASE001"):
        print(" ", e)
