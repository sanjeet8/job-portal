from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User
from ..auth.hashing import hash_password, verify_password
from ..auth.jwt_handler import create_access_token, verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(password)
    user = User(username=username, password=hashed_pwd)
    db.add(user)
    db.commit()
    return {"message": "User registered"}

@router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token}

@router.get("/protected")
def protected_route(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"message": f"Hello {payload['sub']}, you are authorized!"}