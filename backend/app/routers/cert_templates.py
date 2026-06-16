from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CertificateTemplate
from app.schemas import CertTemplateCreate, CertTemplateUpdate, CertTemplateResponse
from app.auth import require_admin

router = APIRouter(prefix="/api/cert-templates", tags=["cert-templates"])


@router.get("/", response_model=list[CertTemplateResponse])
def list_cert_templates(db: Session = Depends(get_db)):
    return db.query(CertificateTemplate).order_by(CertificateTemplate.category, CertificateTemplate.name).all()


@router.post("/", response_model=CertTemplateResponse)
def create_cert_template(data: CertTemplateCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    existing = db.query(CertificateTemplate).filter(CertificateTemplate.name == data.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Certificate template already exists")
    tmpl = CertificateTemplate(name=data.name, category=data.category)
    db.add(tmpl)
    db.commit()
    db.refresh(tmpl)
    return tmpl


@router.put("/{template_id}", response_model=CertTemplateResponse)
def update_cert_template(template_id: int, data: CertTemplateUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    tmpl = db.query(CertificateTemplate).filter(CertificateTemplate.id == template_id).first()
    if not tmpl:
        raise HTTPException(status_code=404, detail="Certificate template not found")
    if data.name is not None:
        tmpl.name = data.name
    if data.category is not None:
        tmpl.category = data.category
    db.commit()
    db.refresh(tmpl)
    return tmpl


@router.delete("/{template_id}")
def delete_cert_template(template_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    tmpl = db.query(CertificateTemplate).filter(CertificateTemplate.id == template_id).first()
    if not tmpl:
        raise HTTPException(status_code=404, detail="Certificate template not found")
    db.delete(tmpl)
    db.commit()
    return {"ok": True}
