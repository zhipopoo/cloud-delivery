import hashlib
import os
import base64
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AdminUser


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Hash a password with PBKDF2-SHA256. Returns (hash, salt)."""
    if salt is None:
        salt = base64.b64encode(os.urandom(32)).decode()
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200000)
    return (base64.b64encode(dk).decode(), salt)


def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    """Verify a password against stored hash + salt."""
    computed, _ = hash_password(password, salt)
    return computed == stored_hash


def require_admin(authorization: str = Header(None)):
    """Validate Bearer token against admin_users table.
    Token format: base64(username:session_key) — simple self-contained token.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")

    token = authorization.replace("Bearer ", "")
    db: Session = next(get_db())

    # Token = base64(username)
    try:
        username = base64.b64decode(token).decode()
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid token")

    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    return username
