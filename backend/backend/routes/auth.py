from fastapi import APIRouter, HTTPException
from schemas.auth_schema import LoginRequest, LoginResponse

router = APIRouter()

users = [
    {
        "username": "manohar",
        "password": "1234",
        "role": "investigator"
    }
]

@router.post("/auth/login", response_model=LoginResponse)
def login(credentials: LoginRequest):

    for user in users:
        if (
            user["username"] == credentials.username and
            user["password"] == credentials.password
        ):
            return LoginResponse(
                access_token="demo_token_123",
                token_type="bearer",
                role=user["role"]
            )

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )