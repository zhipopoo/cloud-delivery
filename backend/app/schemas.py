from pydantic import BaseModel
from typing import Optional


class CertificateItem(BaseModel):
    name: str
    category: str
    status: str
    issue_date: str = ""
    expiry_date: str = ""
    file_url: str = ""


class LanguageLevel(BaseModel):
    cantonese: str = "N/A"
    english: str = "N/A"
    mandarin: str = "N/A"


class MemberCreate(BaseModel):
    name: str
    avatar_seed: str
    role: str
    team: str
    title: str = ""
    bio: str = ""
    welink_id: str = ""
    photo_url: str = ""
    skills: list[str] = []
    certificates: list[CertificateItem] = []
    languages: LanguageLevel = LanguageLevel()
    fans_count: int = 0


class MemberUpdate(BaseModel):
    name: str | None = None
    avatar_seed: str | None = None
    role: str | None = None
    team: str | None = None
    title: str | None = None
    bio: str | None = None
    welink_id: str | None = None
    photo_url: str | None = None
    skills: list[str] | None = None
    certificates: list[CertificateItem] | None = None
    languages: LanguageLevel | None = None
    fans_count: int | None = None


class MemberResponse(BaseModel):
    id: int
    name: str
    avatar_seed: str
    role: str
    team: str
    title: str
    bio: str
    welink_id: str
    photo_url: str
    skills: list[str]
    certificates: list[CertificateItem]
    languages: LanguageLevel
    fans_count: int

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    client: str = ""
    description: str = ""
    start_date: str
    end_date: str
    status: str = "active"


class ProjectUpdate(BaseModel):
    name: str | None = None
    client: str | None = None
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    status: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    client: str
    description: str
    start_date: str
    end_date: str
    status: str

    class Config:
        from_attributes = True


class AssignmentCreate(BaseModel):
    member_id: int
    project_id: int
    busy_level: str = "green"
    role_in_project: str = ""


class AssignmentUpdate(BaseModel):
    member_id: int | None = None
    project_id: int | None = None
    busy_level: str | None = None
    role_in_project: str | None = None


class AssignmentResponse(BaseModel):
    id: int
    member_id: int
    project_id: int
    busy_level: str
    role_in_project: str
    member_name: Optional[str] = None
    project_name: Optional[str] = None

    class Config:
        from_attributes = True


class FanMessageCreate(BaseModel):
    member_id: int
    author_name: str
    content: str


class FanMessageResponse(BaseModel):
    id: int
    member_id: int
    author_name: str
    content: str
    created_at: str

    class Config:
        from_attributes = True