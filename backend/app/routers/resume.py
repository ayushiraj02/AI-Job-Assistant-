from fastapi import APIRouter, HTTPException

from app.schemas import ResumeUploadRequest, ResumeUploadResponse
from app.storage import resume_store

router = APIRouter()


@router.post("/resume", response_model=ResumeUploadResponse)
def upload_resume(payload: ResumeUploadRequest) -> ResumeUploadResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Resume text cannot be empty.")

    resume_store["resume_text"] = text
    return ResumeUploadResponse(message="Resume uploaded successfully.")
