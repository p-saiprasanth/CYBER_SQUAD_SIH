from fastapi import APIRouter
import hashlib

router = APIRouter()


@router.post("/security/hash-evidence")
def hash_evidence(evidence: dict):

    text = evidence.get("text", "")

    hash_value = hashlib.sha256(text.encode()).hexdigest()

    return {
        "original_text": text,
        "sha256_hash": hash_value
    }


@router.post("/security/verify-evidence")
def verify_evidence(data: dict):

    text = data.get("text", "")
    received_hash = data.get("hash", "")

    calculated_hash = hashlib.sha256(text.encode()).hexdigest()

    return {
        "verified": calculated_hash == received_hash,
        "calculated_hash": calculated_hash,
        "received_hash": received_hash
    }