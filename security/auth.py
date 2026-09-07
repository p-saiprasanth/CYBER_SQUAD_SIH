"""
auth.py
-------
Phase 1 — Security Architecture: Authentication & RBAC.

Minimal but real RBAC: three roles (INVESTIGATOR, ADMIN, ANALYST), a
permission table, password hashing with a per-user salt, and a
require_role decorator to protect functions/endpoints.

This is a hackathon-appropriate implementation (no external deps) —
in production, swap the token scheme for real JWTs and password hashing
for bcrypt/argon2, but the interface below stays stable.
"""

import hashlib
import secrets
from datetime import datetime, timezone
from functools import wraps


# ---------------------------------------------------------------------------
# Roles & permissions
# ---------------------------------------------------------------------------

ROLES = {"INVESTIGATOR", "ADMIN", "ANALYST"}

# What each role is allowed to do. Investigators can work cases and evidence
# but CANNOT perform administrative actions (user management, system config).
PERMISSIONS = {
    "ADMIN": {
        "manage_users", "manage_roles", "view_all_cases", "create_case",
        "upload_evidence", "verify_evidence", "view_graph", "run_ai_query",
        "export_report", "view_audit_logs", "configure_system",
    },
    "INVESTIGATOR": {
        "view_all_cases", "create_case", "upload_evidence", "verify_evidence",
        "view_graph", "run_ai_query", "export_report",
    },
    "ANALYST": {
        "view_all_cases", "view_graph", "run_ai_query",
    },
}


def has_permission(role: str, permission: str) -> bool:
    """Check whether a role is allowed to perform a given action."""
    if role not in PERMISSIONS:
        return False
    return permission in PERMISSIONS[role]


# ---------------------------------------------------------------------------
# Password hashing (salted SHA-256 — adequate for hackathon MVP)
# ---------------------------------------------------------------------------

def hash_password(password: str, salt: str = None) -> tuple:
    """Return (salt, hash) for a password. Generates a new salt if not given."""
    salt = salt or secrets.token_hex(16)
    digest = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt, digest


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """Check a plaintext password against a stored salt+hash."""
    _, digest = hash_password(password, salt)
    return digest == expected_hash


# ---------------------------------------------------------------------------
# In-memory user store + session tokens (demo only)
# ---------------------------------------------------------------------------

_users = {}     # username -> {"salt", "hash", "role", "user_id"}
_sessions = {}  # token -> {"user_id", "role", "issued_at"}


def register_user(user_id: str, username: str, password: str, role: str):
    """Create a user with a given role. Raises if the role is invalid."""
    if role not in ROLES:
        raise ValueError(f"Invalid role: {role!r}. Must be one of {ROLES}.")
    salt, digest = hash_password(password)
    _users[username] = {"user_id": user_id, "salt": salt, "hash": digest, "role": role}


def authenticate_user(username: str, password: str) -> dict:
    """
    Verify credentials and issue a session token.

    Returns
    -------
    dict
        {"success": True, "token": ..., "role": ..., "user_id": ...}
        or {"success": False, "message": "..."}
    """
    user = _users.get(username)
    if not user or not verify_password(password, user["salt"], user["hash"]):
        return {"success": False, "message": "Invalid username or password"}

    token = secrets.token_hex(24)
    _sessions[token] = {
        "user_id": user["user_id"],
        "role": user["role"],
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }
    return {"success": True, "token": token, "role": user["role"], "user_id": user["user_id"]}


def get_session(token: str) -> dict:
    """Look up the session (user_id, role) attached to a token."""
    return _sessions.get(token)


# ---------------------------------------------------------------------------
# Authorization decorator
# ---------------------------------------------------------------------------

class PermissionDenied(Exception):
    pass


def require_permission(permission: str):
    """
    Decorator that protects a function so it only runs if the caller's
    token grants the required permission.

    Usage:
        @require_permission("upload_evidence")
        def upload_evidence(token, ...):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(token, *args, **kwargs):
            session = get_session(token)
            if not session:
                raise PermissionDenied("Invalid or expired session token")
            if not has_permission(session["role"], permission):
                raise PermissionDenied(
                    f"Role '{session['role']}' is not permitted to '{permission}'"
                )
            return func(token, *args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    # Set up demo users
    register_user("U001", "investigator1", "pass123", "INVESTIGATOR")
    register_user("U002", "admin1", "adminpass", "ADMIN")

    # Investigator logs in
    login = authenticate_user("investigator1", "pass123")
    print("Investigator login:", login)
    inv_token = login["token"]

    # Investigator tries an allowed action
    @require_permission("upload_evidence")
    def upload_evidence(token, evidence_id):
        return f"Evidence {evidence_id} uploaded."

    print(upload_evidence(inv_token, "E001"))

    # Investigator tries an admin-only action -> should be denied
    @require_permission("manage_users")
    def manage_users(token):
        return "User management panel opened."

    try:
        manage_users(inv_token)
    except PermissionDenied as e:
        print("Blocked as expected:", e)
