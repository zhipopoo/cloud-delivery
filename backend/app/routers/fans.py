from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FanMessage, Member
from app.schemas import FanMessageCreate, FanMessageResponse
from datetime import datetime

router = APIRouter(prefix="/api/fans", tags=["fans"])


@router.get("/{member_id}", response_model=list[FanMessageResponse])
def get_messages(member_id: int, db: Session = Depends(get_db)):
    return db.query(FanMessage).filter(FanMessage.member_id == member_id).order_by(FanMessage.created_at.desc()).all()


@router.post("/", response_model=FanMessageResponse)
def post_message(data: FanMessageCreate, db: Session = Depends(get_db)):
    msg = FanMessage(
        member_id=data.member_id,
        author_name=data.author_name,
        content=data.content,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(msg)
    member = db.query(Member).filter(Member.id == data.member_id).first()
    if member:
        member.fans_count = (member.fans_count or 0) + 1
    db.commit()
    db.refresh(msg)
    return msg