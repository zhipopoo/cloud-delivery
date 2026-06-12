from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Member, Project, ProjectAssignment, FanMessage
import json


def seed_data():
    db: Session = SessionLocal()
    if db.query(Member).first():
        db.close()
        return

    members_data = [
        {
            "name": "Zhang Wei", "avatar_seed": "zhangwei", "role": "TMO Lead",
            "team": "TMO", "title": "Senior Cloud Architect",
            "bio": "10+ years in cloud infrastructure. Led 50+ enterprise migrations.",
            "skills": ["Kubernetes", "Terraform", "Python", "Network Security", "CCE"],
            "certificates": [{"name": "HCIE-Cloud", "category": "technical", "status": "active"}, {"name": "PMP", "category": "general", "status": "active"}],
            "languages": {"cantonese": "Fluent", "english": "Professional", "mandarin": "Native"},
            "fans_count": 42,
            "welink_id": "zhangwei001",
        },
        {
            "name": "Li Na", "avatar_seed": "lina", "role": "PMO Manager",
            "team": "PMO", "title": "Project Delivery Director",
            "bio": "PMP certified. Expert in large-scale project governance and delivery.",
            "skills": ["Project Governance", "Risk Management", "Agile", "SAFe", "Jira"],
            "certificates": [{"name": "PMP", "category": "general", "status": "active", "issue_date": "2022-06-15", "expiry_date": "2027-06-15", "file_url": ""}, {"name": "SAFe Agilist", "category": "general", "status": "active", "issue_date": "2023-03-20", "expiry_date": "2025-03-20", "file_url": ""}],
            "languages": {"cantonese": "Basic", "english": "Fluent", "mandarin": "Native"},
            "fans_count": 38,
            "welink_id": "lina002",
        },
        {
            "name": "Wang Jun", "avatar_seed": "wangjun", "role": "TMO Engineer",
            "team": "TMO", "title": "Cloud Deployment Specialist",
            "bio": "Focused on automated deployment pipelines and CI/CD optimization.",
            "skills": ["CI/CD", "Docker", "Jenkins", "Ansible", "Huawei Cloud"],
            "certificates": [{"name": "HCIP-Cloud", "category": "technical", "status": "active", "issue_date": "2024-01-10", "expiry_date": "2027-01-10", "file_url": ""}, {"name": "AWS SAA", "category": "technical", "status": "expired", "issue_date": "2021-05-20", "expiry_date": "2024-05-20", "file_url": ""}],
            "languages": {"cantonese": "N/A", "english": "Intermediate", "mandarin": "Native"},
            "fans_count": 25,
            "welink_id": "wangjun003",
        },
        {
            "name": "Chen Xiao", "avatar_seed": "chenxiao", "role": "Management",
            "team": "Management", "title": "Delivery VP",
            "bio": "Strategic leader driving digital transformation for Fortune 500 clients.",
            "skills": ["Strategic Planning", "Client Relations", "Digital Transformation", "Budget Control"],
            "certificates": [{"name": "HCIE-Cloud", "category": "technical", "status": "active", "issue_date": "2023-09-01", "expiry_date": "2026-09-01", "file_url": ""}, {"name": "ITIL v4", "category": "general", "status": "active", "issue_date": "2022-08-10", "expiry_date": "2025-08-10", "file_url": ""}],
            "languages": {"cantonese": "Fluent", "english": "Native", "mandarin": "Fluent"},
            "fans_count": 67,
            "welink_id": "chenxiao004",
        },
        {
            "name": "Liu Yang", "avatar_seed": "liuyang", "role": "PMO Lead",
            "team": "PMO", "title": "Senior Project Manager",
            "bio": "Delivered 30+ cloud migration projects on time and under budget.",
            "skills": ["Cloud Migration", "Stakeholder Management", "MS Project", "Confluence"],
            "certificates": [{"name": "PMP", "category": "general", "status": "active", "issue_date": "2021-11-15", "expiry_date": "2026-11-15", "file_url": ""}, {"name": "HCIP-Cloud Service", "category": "technical", "status": "active", "issue_date": "2024-02-28", "expiry_date": "2027-02-28", "file_url": ""}],
            "languages": {"cantonese": "Intermediate", "english": "Professional", "mandarin": "Native"},
            "fans_count": 31,
            "welink_id": "liuyang005",
        },
        {
            "name": "Zhao Mei", "avatar_seed": "zhaomei", "role": "TMO Engineer",
            "team": "TMO", "title": "Security & Compliance Engineer",
            "bio": "Cloud security specialist with deep expertise in compliance frameworks.",
            "skills": ["Cloud Security", "Compliance", "WAF", "DDoS Protection", "ISO 27001"],
            "certificates": [{"name": "CISSP", "category": "technical", "status": "active", "issue_date": "2023-07-15", "expiry_date": "2026-07-15", "file_url": ""}, {"name": "HCIE-Security", "category": "technical", "status": "active", "issue_date": "2024-03-01", "expiry_date": "2027-03-01", "file_url": ""}],
            "languages": {"cantonese": "Basic", "english": "Fluent", "mandarin": "Native"},
            "fans_count": 29,
            "welink_id": "zhaomei006",
        },
    ]

    for md in members_data:
        m = Member(
            name=md["name"], avatar_seed=md["avatar_seed"], role=md["role"],
            team=md["team"], title=md["title"], bio=md["bio"],
            welink_id=md.get("welink_id", ""),
            photo_url=md.get("photo_url", ""),
            skills=json.dumps(md["skills"]),
            certificates=json.dumps(md["certificates"]),
            languages=json.dumps(md["languages"]),
            fans_count=md["fans_count"],
        )
        db.add(m)

    db.commit()

    projects_data = [
        {"name": "Bank of China Cloud Migration", "client": "Bank of China", "description": "Full cloud migration of core banking systems", "start_date": "2026-01-15", "end_date": "2026-06-30", "status": "active"},
        {"name": "China Mobile 5G Core", "client": "China Mobile", "description": "5G core network cloud deployment", "start_date": "2026-03-01", "end_date": "2026-09-30", "status": "active"},
        {"name": "PetroChina Data Platform", "client": "PetroChina", "description": "Big data platform on Huawei Cloud", "start_date": "2026-02-01", "end_date": "2026-08-15", "status": "active"},
        {"name": "CMB AI Model Hub", "client": "China Merchants Bank", "description": "AI model deployment and serving platform", "start_date": "2026-04-01", "end_date": "2026-12-31", "status": "active"},
    ]

    for pd in projects_data:
        p = Project(**pd)
        db.add(p)

    db.commit()

    assignments = [
        {"member_id": 1, "project_id": 1, "busy_level": "red", "role_in_project": "Tech Lead"},
        {"member_id": 2, "project_id": 1, "busy_level": "yellow", "role_in_project": "PM"},
        {"member_id": 3, "project_id": 2, "busy_level": "green", "role_in_project": "Deploy Engineer"},
        {"member_id": 4, "project_id": 2, "busy_level": "red", "role_in_project": "Sponsor"},
        {"member_id": 5, "project_id": 3, "busy_level": "yellow", "role_in_project": "PM"},
        {"member_id": 6, "project_id": 4, "busy_level": "red", "role_in_project": "Security Lead"},
        {"member_id": 1, "project_id": 3, "busy_level": "green", "role_in_project": "Advisor"},
        {"member_id": 3, "project_id": 1, "busy_level": "yellow", "role_in_project": "CI/CD Lead"},
    ]

    for ad in assignments:
        a = ProjectAssignment(**ad)
        db.add(a)

    fan_messages = [
        {"member_id": 1, "author_name": "Client CTO", "content": "Zhang Wei's architecture design saved us 40% on infrastructure costs!", "created_at": "2026-05-10T08:30:00"},
        {"member_id": 2, "author_name": "Team Lead", "content": "Li Na keeps every milestone on track. Best PMO ever!", "created_at": "2026-05-12T14:20:00"},
        {"member_id": 4, "author_name": "VP of Sales", "content": "Chen Xiao's strategic vision helped us win the biggest deal this year.", "created_at": "2026-05-15T09:00:00"},
        {"member_id": 6, "author_name": "CISO", "content": "Zhao Mei's security audit found critical vulnerabilities before go-live.", "created_at": "2026-05-18T16:45:00"},
    ]

    for fd in fan_messages:
        fm = FanMessage(**fd)
        db.add(fm)

    db.commit()
    db.close()