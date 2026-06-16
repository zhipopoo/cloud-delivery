import base64
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AdminUser
from app.schemas import LoginRequest, LoginResponse
from app.auth import verify_password, require_admin

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(AdminUser).filter(AdminUser.username == data.username).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid username or password")

    # password_hash stored as "salt:hash"
    parts = user.password_hash.split(":", 1)
    if len(parts) != 2:
        raise HTTPException(status_code=500, detail="Invalid stored credential format")

    salt, stored_hash = parts
    if not verify_password(data.password, salt, stored_hash):
        raise HTTPException(status_code=403, detail="Invalid username or password")

    # Token = base64(username)
    token = base64.b64encode(user.username.encode()).decode()
    return {"token": token, "username": user.username}


@router.get("/me")
def whoami(username: str = Depends(require_admin)):
    return {"username": username}
