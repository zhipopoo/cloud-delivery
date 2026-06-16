from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Skill
from app.schemas import SkillCreate, SkillUpdate, SkillResponse
from app.auth import require_admin

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("/", response_model=list[SkillResponse])
def list_skills(db: Session = Depends(get_db)):
    return db.query(Skill).order_by(Skill.category, Skill.name).all()


@router.post("/", response_model=SkillResponse)
def create_skill(data: SkillCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    existing = db.query(Skill).filter(Skill.name == data.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Skill already exists")
    skill = Skill(name=data.name, category=data.category)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.put("/{skill_id}", response_model=SkillResponse)
def update_skill(skill_id: int, data: SkillUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    if data.name is not None:
        skill.name = data.name
    if data.category is not None:
        skill.category = data.category
    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"ok": True}
