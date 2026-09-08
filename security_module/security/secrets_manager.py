"""
secrets_manager.py
-------------------
Phase 1 (remainder) — Secure secrets handling.

Rule: secrets (DB passwords, API keys, JWT signing keys, Neo4j credentials)
must NEVER be hardcoded in source files or committed to git. They are
read from environment variables, with a clear error if something required
is missing — instead of silently falling back to an insecure default.

For local dev, put values in a `.env` file (which must be in .gitignore)
and load it with a library like python-dotenv; in production, these come
from the platform's secrets manager (e.g. Docker secrets, cloud KMS).
"""

import os


REQUIRED_SECRETS = [
    "JWT_SECRET_KEY",
    "NEO4J_PASSWORD",
    "DATABASE_URL",
]


class MissingSecretError(Exception):
    pass


def get_secret(name: str, required: bool = True, default: str = None) -> str:
    """
    Fetch a secret from environment variables.

    Parameters
    ----------
    name     : the environment variable name, e.g. "JWT_SECRET_KEY"
    required : if True, raises when the value is missing instead of
               silently returning a default (fail loud, not quiet)
    default  : fallback value, only used when required=False
    """
    value = os.environ.get(name, default)
    if required and not value:
        raise MissingSecretError(
            f"Required secret '{name}' is not set. "
            f"Set it as an environment variable (see .env.example)."
        )
    return value


def check_required_secrets() -> dict:
    """
    Startup check: verify all required secrets are present before the
    app starts serving traffic. Call this once at application boot.
    """
    status = {}
    missing = []
    for name in REQUIRED_SECRETS:
        present = bool(os.environ.get(name))
        status[name] = "set" if present else "MISSING"
        if not present:
            missing.append(name)

    if missing:
        raise MissingSecretError(f"Missing required secrets at startup: {missing}")

    return status


if __name__ == "__main__":
    # Demo: simulate a missing secret
    try:
        get_secret("JWT_SECRET_KEY")
    except MissingSecretError as e:
        print("Expected failure (no env var set):", e)

    # Demo: simulate it being set
    os.environ["JWT_SECRET_KEY"] = "demo-only-not-a-real-secret"
    print("Now retrieved:", get_secret("JWT_SECRET_KEY"))
