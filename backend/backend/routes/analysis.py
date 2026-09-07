from fastapi import APIRouter

router = APIRouter()

@router.post("/cases/{case_id}/process")
def process_case(case_id: int):
    return {
        "case_id": case_id,
        "status": "Processing completed",
        "suspects_found": 2,
        "risk_score": 85
    }