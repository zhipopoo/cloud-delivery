from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Member
from app.schemas import MemberCreate, MemberUpdate, MemberResponse
import json

router = APIRouter(prefix="/api/members", tags=["members"])


def _parse_member(m: Member) -> dict:
    return {
        "id": m.id,
        "name": m.name,
        "avatar_seed": m.avatar_seed,
        "role": m.role,
        "team": m.team,
        "title": m.title,
        "bio": m.bio,
        "welink_id": m.welink_id or "",
        "photo_url": m.photo_url or "",
        "skills": json.loads(m.skills) if m.skills else [],
        "certificates": json.loads(m.certificates) if m.certificates else [],
        "languages": json.loads(m.languages) if m.languages else {},
        "fans_count": m.fans_count or 0,
    }


@router.get("/", response_model=list[MemberResponse])
def list_members(team: str = None, db: Session = Depends(get_db)):
    q = db.query(Member)
    if team:
        q = q.filter(Member.team == team)
    return [_parse_member(m) for m in q.all()]


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    m = db.query(Member).filter(Member.id == member_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Member not found")
    return _parse_member(m)


@router.post("/", response_model=MemberResponse)
def create_member(data: MemberCreate, db: Session = Depends(get_db)):
    m = Member(
        name=data.name,
        avatar_seed=data.avatar_seed,
        role=data.role,
        team=data.team,
        title=data.title,
        bio=data.bio,
        welink_id=data.welink_id,
        photo_url=data.photo_url,
        skills=json.dumps(data.skills),
        certificates=json.dumps([c.model_dump() for c in data.certificates]),
        languages=json.dumps(data.languages.model_dump()),
        fans_count=data.fans_count,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return _parse_member(m)


@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, data: MemberUpdate, db: Session = Depends(get_db)):
    m = db.query(Member).filter(Member.id == member_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Member not found")

    update_data = data.model_dump(exclude_unset=True)

    # Handle JSON fields
    if "skills" in update_data:
        update_data["skills"] = json.dumps(update_data["skills"])
    if "certificates" in update_data:
        update_data["certificates"] = json.dumps(
            [c.model_dump() if hasattr(c, 'model_dump') else c for c in update_data["certificates"]]
        )
    if "languages" in update_data:
        update_data["languages"] = json.dumps(
            update_data["languages"].model_dump() if hasattr(update_data["languages"], 'model_dump') else update_data["languages"]
        )

    for field, value in update_data.items():
        setattr(m, field, value)

    db.commit()
    db.refresh(m)
    return _parse_member(m)


@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    m = db.query(Member).filter(Member.id == member_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(m)
    db.commit()
    return {"ok": True}
