from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    return {
        "total_cases": 1,
        "total_evidence": 2,
        "processed_cases": 1,
        "high_risk_cases": 1
    }