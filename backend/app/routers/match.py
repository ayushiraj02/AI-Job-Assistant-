from fastapi import APIRouter, HTTPException

from app.schemas import MatchRequest, MatchResponse
from app.services.jobs_service import get_job_by_id
from app.services.matcher import calculate_match_percentage
from app.storage import resume_store

router = APIRouter()


@router.post("/match", response_model=MatchResponse)
def get_match_score(payload: MatchRequest) -> MatchResponse:
    resume_text = resume_store.get("resume_text", "").strip()
    if not resume_text:
        raise HTTPException(status_code=400, detail="Please upload resume text first.")

    job_description = payload.job_description.strip() if payload.job_description else ""

    if payload.job_id is not None:
        job = get_job_by_id(payload.job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found.")
        job_description = job.description

    if not job_description:
        raise HTTPException(
            status_code=400,
            detail="Provide either job_description or a valid job_id.",
        )

    score = calculate_match_percentage(resume_text, job_description)
    return MatchResponse(match_percentage=score)
