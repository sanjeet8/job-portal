from celery import Celery

# Create Celery instance (connects to Redis)
celery_app = Celery(
    "notification_tasks",
    broker="redis://redis:6379/0",  # internal Docker hostname
    backend="redis://redis:6379/0"
)

@celery_app.task
def send_email_notification(user_email: str, job_id: int):
    print(f"📧 Email sent to {user_email} for Job #{job_id}")
    return f"Email sent to {user_email} for Job #{job_id}"
