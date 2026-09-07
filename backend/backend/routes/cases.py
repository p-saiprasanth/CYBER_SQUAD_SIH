from fastapi import APIRouter, HTTPException
from schemas.case_schema import CaseCreate, CaseResponse
from services.database import (
    create_case,
    get_all_cases,
    get_case_by_id
)

router = APIRouter()


@router.get("/cases")
def get_cases():
    return get_all_cases()


@router.post("/cases", response_model=CaseResponse)
def add_case(case: CaseCreate):
    return create_case(case.model_dump())


@router.get("/cases/{case_id}")
def get_case(case_id: int):

    case = get_case_by_id(case_id)

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return case