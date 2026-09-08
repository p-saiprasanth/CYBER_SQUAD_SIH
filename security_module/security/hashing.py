"""
hashing.py
----------
Phase 3 — Hashing.

Generates SHA-256 fingerprints for evidence files and builds the
integrity metadata record that gets stored (later, on the ledger).

We NEVER store raw evidence on the ledger — only the hash + metadata.
"""

import hashlib
from datetime import datetime, timezone


CHUNK_SIZE = 8192  # read in chunks so large files (videos, PDFs) don't blow up memory


def hash_evidence(file_path: str) -> str:
    """
    Compute the SHA-256 hash of a file.

    Parameters
    ----------
    file_path : str
        Path to the evidence file (any type — image, PDF, doc, video, etc).

    Returns
    -------
    str
        Hex-encoded SHA-256 hash of the file's contents.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()


def create_evidence_record(evidence_id: str, case_id: str, file_path: str, action: str) -> dict:
    """
    Build the integrity metadata record for a piece of evidence.
    This is the ONLY thing that should ever be written to the ledger —
    never the raw file itself.

    Parameters
    ----------
    evidence_id : str   e.g. "E001"
    case_id     : str   e.g. "CASE001"
    file_path   : str   path to the evidence file to hash
    action      : str   e.g. "EVIDENCE_REGISTERED"

    Returns
    -------
    dict
        {
          "evidence_id": ...,
          "case_id": ...,
          "hash": ...,
          "timestamp": ...,
          "action": ...
        }
    """
    return {
        "evidence_id": evidence_id,
        "case_id": case_id,
        "hash": hash_evidence(file_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
    }


if __name__ == "__main__":
    # quick demo
    import tempfile, os

    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp:
        tmp.write("This is sample evidence content.")
        path = tmp.name

    record = create_evidence_record("E001", "CASE001", path, "EVIDENCE_REGISTERED")
    print("Evidence record created:")
    print(record)

    os.remove(path)
