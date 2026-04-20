from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auto_apply import router as auto_apply_router
from app.routers.jobs import router as jobs_router
from app.routers.match import router as match_router
from app.routers.resume import router as resume_router

app = FastAPI(title="AI Job Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router, prefix="/api", tags=["resume"])
app.include_router(jobs_router, prefix="/api", tags=["jobs"])
app.include_router(match_router, prefix="/api", tags=["match"])
app.include_router(auto_apply_router, prefix="/api", tags=["auto-apply"])


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "AI Job Assistant backend is running."}
