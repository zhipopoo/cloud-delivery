from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AdminUser
from app.schemas import AdminUserCreate, AdminUserResponse
from app.auth import require_admin, hash_password

router = APIRouter(prefix="/api/admins", tags=["admins"])


@router.get("/", response_model=list[AdminUserResponse])
def list_admins(db: Session = Depends(get_db), _=Depends(require_admin)):
    return db.query(AdminUser).order_by(AdminUser.username).all()


@router.post("/", response_model=AdminUserResponse)
def create_admin(data: AdminUserCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    existing = db.query(AdminUser).filter(AdminUser.username == data.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="Admin user already exists")
    if len(data.password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters")

    h, salt = hash_password(data.password)
    user = AdminUser(username=data.username, password_hash=f"{salt}:{h}")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{admin_id}")
def delete_admin(admin_id: int, db: Session = Depends(get_db), current_user: str = Depends(require_admin)):
    user = db.query(AdminUser).filter(AdminUser.id == admin_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Admin user not found")
    if user.username == current_user:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    # Prevent deleting the last admin
    count = db.query(AdminUser).count()
    if count <= 1:
        raise HTTPException(status_code=400, detail="Cannot delete the last admin user")

    db.delete(user)
    db.commit()
    return {"ok": True}
