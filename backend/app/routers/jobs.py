from fastapi import APIRouter

from app.schemas import Job
from app.services.jobs_service import get_jobs

router = APIRouter()


@router.get("/jobs", response_model=list[Job])
def list_jobs() -> list[Job]:
    return get_jobs()
