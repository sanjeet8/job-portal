from fastapi import FastAPI, BackgroundTasks
from app.tasks import send_email_notification

app = FastAPI(
    title="Notification Service",
    description="Sends email notifications when job is applied",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Notification Service is live!"}

@app.post("/notify/")
def notify(email: str, job_id: int, background_tasks: BackgroundTasks):
    # Celery task (async)
    send_email_notification.delay(email, job_id)
    return {"message": f"Notification queued for {email}"}
