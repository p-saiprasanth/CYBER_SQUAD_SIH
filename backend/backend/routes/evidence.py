from fastapi import APIRouter

router = APIRouter()

# Temporary storage
evidences = []

@router.post("/cases/{case_id}/evidence")
def add_evidence(case_id: int, evidence: dict):
    evidence["case_id"] = case_id
    evidence["id"] = len(evidences) + 1
    evidences.append(evidence)
    return evidence


@router.get("/cases/{case_id}/evidence")
def get_evidence(case_id: int):
    result = []

    for e in evidences:
        if e["case_id"] == case_id:
            result.append(e)

    return result