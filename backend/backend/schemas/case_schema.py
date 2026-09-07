from pydantic import BaseModel, Field
from datetime import datetime

class CaseCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    crime_type: str = Field(..., min_length=3)
    created_at: datetime

class CaseResponse(CaseCreate):
    id: int