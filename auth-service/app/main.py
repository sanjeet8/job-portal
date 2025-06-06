from fastapi import FastAPI
from .database import Base, engine
from .routes import auth

app = FastAPI(
    title="Authentication Service",
    description="Handles Authentication",
    root_path="/auth",
    version="1.0.0"
)

# Create tables in SQLite
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(auth.router)
