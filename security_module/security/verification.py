"""
verification.py
----------------
Phase 3 — Verification.

Re-hashes a file and compares it against a previously stored hash to
detect tampering. This is the core trust primitive of the whole module:

    original_hash != new_hash  -->  tampering detected
"""

from security.hashing import hash_evidence


def verify_evidence(file_path: str, stored_hash: str) -> dict:
    """
    Verify that a file's current contents match its previously recorded hash.

    Parameters
    ----------
    file_path   : str   path to the evidence file to re-check
    stored_hash : str   the hash that was recorded when evidence was registered

    Returns
    -------
    dict
        {
          "verified": True/False,
          "message": "✓ Evidence verified" | "⚠ Evidence integrity compromised",
          "current_hash": ...,
          "stored_hash": ...
        }
    """
    current_hash = hash_evidence(file_path)
    verified = current_hash == stored_hash

    return {
        "verified": verified,
        "message": "✓ Evidence verified" if verified else "⚠ Evidence integrity compromised",
        "current_hash": current_hash,
        "stored_hash": stored_hash,
    }


if __name__ == "__main__":
    import tempfile, os
    from security.hashing import create_evidence_record

    # Create sample evidence
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp:
        tmp.write("Original evidence content.")
        path = tmp.name

    record = create_evidence_record("E001", "CASE001", path, "EVIDENCE_REGISTERED")
    print("Registered:", record)

    # Case 1: verify unchanged file
    result = verify_evidence(path, record["hash"])
    print("\nVerify (unchanged file):", result["message"])

    # Case 2: tamper with the file, then verify again
    with open(path, "a") as f:
        f.write(" ...tampered content added.")

    result = verify_evidence(path, record["hash"])
    print("Verify (tampered file):  ", result["message"])

    os.remove(path)
