from fastapi import APIRouter, HTTPException

from app.schemas import AutoApplyResponse
from app.services.auto_apply_service import get_applied_jobs, run_auto_apply
from app.storage import resume_store

router = APIRouter()


@router.post("/auto-apply", response_model=AutoApplyResponse)
def auto_apply_jobs() -> AutoApplyResponse:
    resume_text = resume_store.get("resume_text", "").strip()
    if not resume_text:
        raise HTTPException(status_code=400, detail="Please upload resume text first.")

    applied_jobs = run_auto_apply(resume_text)
    return AutoApplyResponse(applied_jobs=applied_jobs)


@router.get("/applied-jobs", response_model=AutoApplyResponse)
def list_applied_jobs() -> AutoApplyResponse:
    return AutoApplyResponse(applied_jobs=get_applied_jobs())
