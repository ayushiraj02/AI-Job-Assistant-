from fastapi import APIRouter

from app.schemas import CoverLetterRequest, CoverLetterResponse
from app.services.cover_letter_service import generate_cover_letter

router = APIRouter()


@router.post("/cover-letter", response_model=CoverLetterResponse)
def create_cover_letter(payload: CoverLetterRequest) -> CoverLetterResponse:
    letter = generate_cover_letter(
        resume_text=payload.resume_text,
        job_title=payload.job_title,
        job_description=payload.job_description,
    )
    return CoverLetterResponse(cover_letter=letter)
