from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    avatar_seed = Column(String(64), nullable=False)
    role = Column(String(64), nullable=False)
    team = Column(String(64), nullable=False)
    title = Column(String(128), default="")
    bio = Column(Text, default="")
    welink_id = Column(String(64), default="")
    photo_url = Column(String(512), default="")
    skills = Column(Text, default="[]")
    certificates = Column(Text, default="[]")
    languages = Column(Text, default="{}")
    fans_count = Column(Integer, default=0)

    project_assignments = relationship("ProjectAssignment", back_populates="member")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    client = Column(String(128), default="")
    description = Column(Text, default="")
    start_date = Column(String(32), nullable=False)
    end_date = Column(String(32), nullable=False)
    status = Column(String(32), default="active")

    assignments = relationship("ProjectAssignment", back_populates="project")


class ProjectAssignment(Base):
    __tablename__ = "project_assignments"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    busy_level = Column(String(16), default="green")
    role_in_project = Column(String(64), default="")

    member = relationship("Member", back_populates="project_assignments")
    project = relationship("Project", back_populates="assignments")


class FanMessage(Base):
    __tablename__ = "fan_messages"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    author_name = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(String(32), nullable=False)