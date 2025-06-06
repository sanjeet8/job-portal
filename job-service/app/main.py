from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from app.routes import job_router

app = FastAPI(
    title="Job Service",
    description="Handles job listings and applications",
    root_path="/jobs",
    version="1.0.0"
)

# This tells Swagger to add "Authorize" button
security = HTTPBearer()

app.include_router(
    job_router,
    #prefix="/jobs",
    dependencies=[Depends(security)]
)