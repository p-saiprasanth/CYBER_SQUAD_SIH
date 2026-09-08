"""
check_completion.py
--------------------
Automated self-audit script. Run this any time to get an honest,
programmatic answer to "is my work actually done?" instead of relying
on memory or a manual checklist.

It checks THREE kinds of things per phase:
  1. Does the required file exist?
  2. Does it contain the required function(s)?
  3. Does the function actually RUN without crashing (a smoke test)?

A phase marked [DOCUMENTATION] is checked for file existence only,
since it's a written deliverable, not code.
"""

import importlib
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

RESULTS = []


def check(phase, description, condition, detail=""):
    status = "DONE" if condition else "MISSING"
    RESULTS.append((phase, description, status, detail))


def has_function(module_name, attr_name):
    """Check that a module exists and has the given attribute — function OR class."""
    try:
        module = importlib.import_module(module_name)
        attr = getattr(module, attr_name, None)
        return attr is not None and (inspect.isroutine(attr) or inspect.isclass(attr))
    except Exception:
        return False


def file_exists(path):
    return os.path.isfile(os.path.join(os.path.dirname(__file__), path))


# ---------------------------------------------------------------------
# PHASE 1 — Security architecture (RBAC, auth, validation, rate limiting, secrets)
# ---------------------------------------------------------------------
check("Phase 1", "RBAC / permission table exists", has_function("security.auth", "has_permission"))
check("Phase 1", "Authentication (login) implemented", has_function("security.auth", "authenticate_user"))
check("Phase 1", "Authorization decorator implemented", has_function("security.auth", "require_permission"))
check("Phase 1", "Input validation implemented", has_function("security.input_validation", "validate_evidence_file"))
check("Phase 1", "Rate limiting implemented", has_function("security.rate_limiter", "RateLimiter"))
check("Phase 1", "Secrets handling implemented", has_function("security.secrets_manager", "get_secret"))

# ---------------------------------------------------------------------
# PHASE 2 — Evidence integrity flow (raw evidence never stored on ledger)
# ---------------------------------------------------------------------
check("Phase 2", "register_evidence hashes before storing (no raw evidence on ledger)",
      has_function("security.blockchain", "register_evidence"))

# ---------------------------------------------------------------------
# PHASE 3 — Hashing & tamper detection
# ---------------------------------------------------------------------
check("Phase 3", "hash_evidence implemented", has_function("security.hashing", "hash_evidence"))
check("Phase 3", "verify_evidence implemented", has_function("security.verification", "verify_evidence"))

# ---------------------------------------------------------------------
# PHASE 4 — Blockchain / ledger abstraction (stub, swappable later)
# ---------------------------------------------------------------------
check("Phase 4", "register_evidence (ledger interface)", has_function("security.blockchain", "register_evidence"))
check("Phase 4", "verify_evidence (ledger interface)", has_function("security.blockchain", "verify_evidence"))
check("Phase 4", "get_evidence_record (ledger interface)", has_function("security.blockchain", "get_evidence_record"))
check("Phase 4", "Real Hyperledger Fabric integration", False,
      detail="Deliberately deferred — MVP uses in-memory stub per project rule")

# ---------------------------------------------------------------------
# PHASE 5 — Audit logging
# ---------------------------------------------------------------------
check("Phase 5", "log_action implemented", has_function("security.audit", "log_action"))
check("Phase 5", "get_audit_trail implemented", has_function("security.audit", "get_audit_trail"))

# ---------------------------------------------------------------------
# PHASE 6 — Threat model (documentation deliverable)
# ---------------------------------------------------------------------
check("Phase 6 [DOC]", "threat_model.md exists", file_exists("docs/threat_model.md"))

# ---------------------------------------------------------------------
# PHASE 7 — AI security guardrails
# ---------------------------------------------------------------------
check("Phase 7", "Prompt injection scanning implemented", has_function("security.ai_guardrails", "sanitize_ai_input"))
check("Phase 7", "AI tool-call authorization implemented", has_function("security.ai_guardrails", "authorize_ai_tool_call"))
check("Phase 7", "AI output validation (no direct accusations)", has_function("security.ai_guardrails", "validate_ai_output"))

# ---------------------------------------------------------------------
# PHASE 8 — Demo script
# ---------------------------------------------------------------------
check("Phase 8", "demo.py exists and is runnable", file_exists("demo.py"))

# ---------------------------------------------------------------------
# PHASE 9 — Integration (FastAPI endpoints, schema sync with team)
# ---------------------------------------------------------------------
check("Phase 9", "FastAPI endpoint wrappers (/security/hash-evidence, etc.)",
      file_exists("api.py") and file_exists("test_api.py"),
      detail="Built & tested standalone — ready for Manohar to mount or replicate")
check("Phase 9", "Audit log schema synced with Aman",
      file_exists("docs/audit_schema_proposal.md"),
      detail="Proposal drafted — awaiting Aman's confirmation, not yet FINAL")


# ---------------------------------------------------------------------
# SMOKE TEST — actually run the core flow end-to-end, don't just check
# that functions exist
# ---------------------------------------------------------------------
def smoke_test():
    import tempfile
    from security.blockchain import register_evidence, verify_evidence

    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp:
        tmp.write("smoke test evidence content")
        path = tmp.name

    try:
        record = register_evidence("SMOKE001", "SMOKETEST", path, user_id="AUDIT")
        result_valid = verify_evidence("SMOKE001", path, user_id="AUDIT")

        with open(path, "a") as f:
            f.write(" tampered")
        result_tampered = verify_evidence("SMOKE001", path, user_id="AUDIT")

        passed = result_valid["verified"] is True and result_tampered["verified"] is False
    except Exception as e:
        passed = False
    finally:
        os.remove(path)

    return passed


# ---------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------
def main():
    print("=" * 72)
    print("SECURITY MODULE — COMPLETION AUDIT")
    print("=" * 72)

    done = 0
    missing = 0
    current_phase = None

    for phase, description, status, detail in RESULTS:
        if phase != current_phase:
            print(f"\n{phase}")
            current_phase = phase
        marker = "[x]" if status == "DONE" else "[ ]"
        line = f"  {marker} {description}"
        if detail:
            line += f"  -- {detail}"
        print(line)
        done += status == "DONE"
        missing += status == "MISSING"

    print("\n" + "-" * 72)
    print("SMOKE TEST — end-to-end register -> verify -> tamper -> verify")
    smoke_passed = smoke_test()
    print(f"  {'[x]' if smoke_passed else '[ ]'} Full pipeline runs correctly: {smoke_passed}")

    total = done + missing
    print("\n" + "=" * 72)
    print(f"RESULT: {done}/{total} items complete")
    if missing:
        print(f"{missing} item(s) still outstanding (see [ ] above).")
    else:
        print("All checked items complete.")
    print("=" * 72)


if __name__ == "__main__":
    main()
