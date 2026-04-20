import json
from pathlib import Path

from app.schemas import Job


def get_jobs() -> list[Job]:
    jobs_path = Path(__file__).resolve().parent.parent / "data" / "jobs.json"
    with jobs_path.open("r", encoding="utf-8") as file:
        jobs_raw = json.load(file)
    return [Job(**job) for job in jobs_raw]


def get_job_by_id(job_id: int) -> Job | None:
    for job in get_jobs():
        if job.id == job_id:
            return job
    return None
