from pydantic import BaseModel, Field


class ResumeUploadRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw resume text")


class ResumeUploadResponse(BaseModel):
    message: str


class Job(BaseModel):
    id: int
    title: str
    company: str
    description: str


class MatchRequest(BaseModel):
    job_description: str | None = Field(default=None, description="Job description text")
    job_id: int | None = Field(default=None, description="Optional job id from listings")


class MatchResponse(BaseModel):
    match_percentage: float


class AppliedJob(BaseModel):
    id: int
    title: str
    company: str
    match_percentage: float
    status: str = "Applied"


class AutoApplyResponse(BaseModel):
    applied_jobs: list[AppliedJob]


class CoverLetterRequest(BaseModel):
    resume_text: str = Field(..., min_length=1, description="Resume text")
    job_title: str = Field(..., min_length=1, description="Target job title")
    job_description: str = Field(..., min_length=1, description="Job description")


class CoverLetterResponse(BaseModel):
    cover_letter: str
