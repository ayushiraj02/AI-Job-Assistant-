from app.schemas import AppliedJob
from app.services.jobs_service import get_jobs
from app.services.matcher import calculate_match_percentage
from app.storage import applied_jobs_store

AUTO_APPLY_THRESHOLD = 70.0


def run_auto_apply(resume_text: str) -> list[AppliedJob]:
    jobs = get_jobs()
    existing_ids = {int(job["id"]) for job in applied_jobs_store}

    for job in jobs:
        score = calculate_match_percentage(resume_text, job.description)
        if score <= AUTO_APPLY_THRESHOLD:
            continue
        if job.id in existing_ids:
            continue

        applied_job = AppliedJob(
            id=job.id,
            title=job.title,
            company=job.company,
            match_percentage=score,
            status="Applied",
        )
        applied_jobs_store.append(applied_job.model_dump())
        existing_ids.add(job.id)

    return [AppliedJob(**job) for job in applied_jobs_store]


def get_applied_jobs() -> list[AppliedJob]:
    return [AppliedJob(**job) for job in applied_jobs_store]
