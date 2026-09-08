"""
api.py
------
Phase 9 — Integration layer.

Thin FastAPI wrappers around the already-tested security/ functions.
This is deliberately a THIN layer — all real logic stays in security/*.py;
these endpoints just handle HTTP request/response and call into it.

Built ahead of Manohar's main API so he can either:
  (a) mount this router directly into the main FastAPI app, or
  (b) use it as the exact contract to replicate in his own structure.

Run standalone for testing:
    uvicorn api:app --reload --port 8001
Then see interactive docs at http://localhost:8001/docs
"""

import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException, Depends
from pydantic import BaseModel

from security.auth import authenticate_user, get_session, has_permission, register_user
from security.blockchain import register_evidence, verify_evidence, get_evidence_record
from security.audit import get_audit_trail, log_action
from security.input_validation import validate_id, ValidationError
from security.rate_limiter import login_limiter, verify_limiter

app = FastAPI(title="Criminal Network Intelligence Platform — Security API")


# ---------------------------------------------------------------------
# Bootstrap demo users so the API is testable out of the box.
# Replace with real user management (Phase 1 admin flows) later.
# ---------------------------------------------------------------------
try:
    register_user("U001", "investigator1", "pass123", "INVESTIGATOR")
    register_user("U002", "admin1", "adminpass", "ADMIN")
except Exception:
    pass  # already registered (e.g. on reload)


# ---------------------------------------------------------------------
# Shared auth dependency
# ---------------------------------------------------------------------
def get_current_session(authorization: str = Header(None)) -> dict:
    """
    Expects header:  Authorization: Bearer <token>
    Returns the session dict {user_id, role, issued_at} or raises 401.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header")
    token = authorization.removeprefix("Bearer ").strip()
    session = get_session(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session token")
    return session


def require(session: dict, permission: str):
    if not has_permission(session["role"], permission):
        raise HTTPException(
            status_code=403,
            detail=f"Role '{session['role']}' is not permitted to '{permission}'",
        )


def _save_upload_to_temp(file: UploadFile) -> str:
    suffix = os.path.splitext(file.filename or "")[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        return tmp.name


# ---------------------------------------------------------------------
# Request/response models
# ---------------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    token: str | None = None
    role: str | None = None
    message: str | None = None


# ---------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------
@app.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, x_forwarded_for: str = Header(default="unknown")):
    if not login_limiter.allow(payload.username):
        raise HTTPException(status_code=429, detail="Too many login attempts. Try again shortly.")

    result = authenticate_user(payload.username, payload.password)
    log_action(
        payload.username,
        "LOGIN",
        ip=x_forwarded_for,
        result="SUCCESS" if result["success"] else "FAILED",
    )
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result


# ---------------------------------------------------------------------
# EVIDENCE — hash / register
# ---------------------------------------------------------------------
@app.post("/security/hash-evidence")
async def hash_evidence(
    evidence_id: str = Form(...),
    case_id: str = Form(...),
    file: UploadFile = File(...),
    session: dict = Depends(get_current_session),
):
    require(session, "upload_evidence")

    try:
        validate_id(evidence_id, "evidence_id")
        validate_id(case_id, "case_id")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    tmp_path = _save_upload_to_temp(file)
    try:
        record = register_evidence(evidence_id, case_id, tmp_path, user_id=session["user_id"])
    finally:
        os.remove(tmp_path)

    return record


# ---------------------------------------------------------------------
# EVIDENCE — verify
# ---------------------------------------------------------------------
@app.post("/security/verify-evidence")
async def verify_evidence_endpoint(
    evidence_id: str = Form(...),
    file: UploadFile = File(...),
    session: dict = Depends(get_current_session),
):
    require(session, "verify_evidence")

    if not verify_limiter.allow(session["user_id"]):
        raise HTTPException(status_code=429, detail="Too many verification requests. Slow down.")

    tmp_path = _save_upload_to_temp(file)
    try:
        result = verify_evidence(evidence_id, tmp_path, user_id=session["user_id"])
    finally:
        os.remove(tmp_path)

    return result


# ---------------------------------------------------------------------
# EVIDENCE — fetch ledger record
# ---------------------------------------------------------------------
@app.get("/security/evidence/{evidence_id}")
def get_evidence(evidence_id: str, session: dict = Depends(get_current_session)):
    require(session, "view_all_cases")
    record = get_evidence_record(evidence_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"No record found for {evidence_id}")
    return record


# ---------------------------------------------------------------------
# AUDIT LOGS
# ---------------------------------------------------------------------
@app.get("/audit/logs")
def get_logs(
    case_id: str = None,
    evidence_id: str = None,
    session: dict = Depends(get_current_session),
):
    require(session, "view_audit_logs")
    return get_audit_trail(case_id=case_id, evidence_id=evidence_id)
