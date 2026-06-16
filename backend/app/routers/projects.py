from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, ProjectAssignment
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, AssignmentCreate, AssignmentUpdate, AssignmentResponse
from app.auth import require_admin

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@router.post("/", response_model=ProjectResponse)
def create_project(data: ProjectCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = Project(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(p, field, value)
    db.commit()
    db.refresh(p)
    return p


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    # Also remove related assignments
    db.query(ProjectAssignment).filter(ProjectAssignment.project_id == project_id).delete()
    db.delete(p)
    db.commit()
    return {"ok": True}


@router.get("/calendar")
def calendar_view(db: Session = Depends(get_db)):
    assignments = db.query(ProjectAssignment).all()
    result = []
    for a in assignments:
        result.append({
            "id": a.id,
            "member_id": a.member_id,
            "member_name": a.member.name if a.member else "",
            "project_id": a.project_id,
            "project_name": a.project.name if a.project else "",
            "start": a.project.start_date if a.project else "",
            "end": a.project.end_date if a.project else "",
            "busy_level": a.busy_level,
            "role_in_project": a.role_in_project,
        })
    return result


@router.post("/assign", response_model=AssignmentResponse)
def assign_member(data: AssignmentCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    a = ProjectAssignment(**data.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return {
        "id": a.id,
        "member_id": a.member_id,
        "project_id": a.project_id,
        "busy_level": a.busy_level,
        "role_in_project": a.role_in_project,
        "member_name": a.member.name if a.member else "",
        "project_name": a.project.name if a.project else "",
    }


@router.put("/assign/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(assignment_id: int, data: AssignmentUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    a = db.query(ProjectAssignment).filter(ProjectAssignment.id == assignment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assignment not found")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(a, field, value)
    db.commit()
    db.refresh(a)
    return {
        "id": a.id,
        "member_id": a.member_id,
        "project_id": a.project_id,
        "busy_level": a.busy_level,
        "role_in_project": a.role_in_project,
        "member_name": a.member.name if a.member else "",
        "project_name": a.project.name if a.project else "",
    }


@router.delete("/assign/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    a = db.query(ProjectAssignment).filter(ProjectAssignment.id == assignment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(a)
    db.commit()
    return {"ok": True}
