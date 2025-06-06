# job-service/app/routes.py
from fastapi import APIRouter, Request, HTTPException, status
from app.utils import verify_token
import httpx

job_router = APIRouter()

@job_router.get("/")
def list_jobs():
    return [{"id": 1, "title": "Software Engineer"}, {"id": 2, "title": "DevOps Engineer"}]

@job_router.get("/{job_id}")
def get_job(job_id: int):
    return {"id": job_id, "title": "Software Engineer"}

@job_router.post("/{job_id}/apply")
async def apply_job(job_id: int, request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

    token = auth_header.split(" ")[1]
    user_data = await verify_token(token)

    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token verification failed")
    
    # Extract dummy email (mock for now)
    email = "user@example.com"  # You can return email in token later

    # Call notification-service to send email
    notify_url = "http://notification-service:8003/notify/"
    async with httpx.AsyncClient() as client:
        response = await client.post(notify_url, params={"email": email, "job_id":job_id})

    if response.status_code != 200:
        raise HTTPException(status_code = 500, detail="Failed to send notification")

    return {
        "message": f"{user_data['message']} successfully applied to job {job_id} and notification sent"
    }