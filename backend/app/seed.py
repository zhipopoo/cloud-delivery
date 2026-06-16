from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Member, Project, ProjectAssignment, FanMessage, Skill, CertificateTemplate, AdminUser
from app.auth import hash_password
import json


def derive_skill_category(name: str) -> str:
    mapping = {
        # Cloud & Infra
        "Kubernetes": "Cloud & Infra", "Docker": "Cloud & Infra", "Terraform": "Cloud & Infra",
        "Ansible": "Cloud & Infra", "CCE": "Cloud & Infra", "Huawei Cloud": "Cloud & Infra",
        "CI/CD": "Cloud & Infra", "Jenkins": "Cloud & Infra", "MySQL": "Cloud & Infra",
        "Network": "Cloud & Infra", "VPC": "Cloud & Infra", "VPN": "Cloud & Infra",
        "Cloud Migration": "Cloud & Infra", "Landingzone": "Cloud & Infra",
        "Cloud Desktop": "Cloud & Infra", "Cloud Security": "Cloud & Infra",
        "GaussDB": "Cloud & Infra", "CodeArts": "Cloud & Infra", "MaaS": "Cloud & Infra",
        "Big Data": "Data & AI",
        # Project & Process
        "Project Governance": "Project & Process", "Risk Management": "Project & Process",
        "Agile": "Project & Process", "SAFe": "Project & Process", "Jira": "Project & Process",
        "Confluence": "Project & Process", "MS Project": "Project & Process",
        "Stakeholder Management": "Project & Process",
        # Security & Compliance
        "Cloud Security": "Security & Compliance", "Compliance": "Security & Compliance",
        "WAF": "Security & Compliance", "DDoS Protection": "Security & Compliance",
        "Network Security": "Security & Compliance", "ISO 27001": "Security & Compliance",
        # Data & AI
        "Python": "Data & AI", "Big Data": "Data & AI", "AI Model": "Data & AI",
        "AI": "Data & AI",
        # Business
        "Strategic Planning": "Business", "Client Relations": "Business",
        "Digital Transformation": "Business", "Budget Control": "Business",
    }
    return mapping.get(name, "Other")


def seed_data():
    db: Session = SessionLocal()

    # ── Always seed default admin if no admin users exist ──
    if not db.query(AdminUser).first():
        h, salt = hash_password("admin123")
        db.add(AdminUser(username="admin", password_hash=f"{salt}:{h}"))
        db.commit()

    # ── Seed skills + cert templates from existing member data (always if empty) ──
    if not db.query(Skill).first() or not db.query(CertificateTemplate).first():
        existing_members = db.query(Member).all()
        if existing_members:
            if not db.query(Skill).first():
                all_skills: set[tuple[str, str]] = set()
                for m in existing_members:
                    skills = json.loads(m.skills) if m.skills else []
                    for s in skills:
                        all_skills.add((s, derive_skill_category(s)))
                for name, cat in sorted(all_skills):
                    db.add(Skill(name=name, category=cat))
                db.commit()

            if not db.query(CertificateTemplate).first():
                all_certs: set[tuple[str, str]] = set()
                for m in existing_members:
                    certs = json.loads(m.certificates) if m.certificates else []
                    for c in certs:
                        all_certs.add((c["name"], c["category"]))
                for name, cat in sorted(all_certs):
                    db.add(CertificateTemplate(name=name, category=cat))
                db.commit()

            db.close()
            return

    # ── Skip member/project seed if data already exists ──
    if db.query(Member).first():
        db.close()
        return

    members_data = [
        {
            "name": "Lawrence Qin",
            "avatar_seed": "Lawrence",
            "role": "TMO Lead",
            "team": "TMO",
            "title": "Executive Engineer",
            "bio": "10+ years in cloud infrastructure. Led 50+ enterprise migrations.",
            "skills": ["Kubernetes", "Terraform", "Python", "Network Security", "CCE"],
            "certificates": [{"name": "HCIP", "category": "technical", "status": "active", "issue_date": "", "expiry_date": "", "file_url": ""}],
            "languages": {"cantonese": "Fluent", "english": "Fluent", "mandarin": "Native"},
            "fans_count": 42,
            "welink_id": "00966500",
            "photo_url": "/api/uploads/df70fbeb5be64e62a9321cebdeff9018.jpeg",
        },
        {
            "name": "Niko Zhang",
            "avatar_seed": "Niko",
            "role": "PMO Manager",
            "team": "PMO",
            "title": "Public Cloud PM",
            "bio": "PMP certified. Expert in large-scale project governance and delivery.",
            "skills": ["Project Governance", "Risk Management", "Agile", "SAFe", "Jira"],
            "certificates": [
                {"name": "PMP", "category": "general", "status": "active", "issue_date": "2022-06-15", "expiry_date": "2027-06-15", "file_url": ""},
                {"name": "Scrum Master", "category": "general", "status": "active", "issue_date": "2016-03-12", "expiry_date": "2027-07-04", "file_url": ""},
                {"name": "ITIL Foundation", "category": "technical", "status": "active", "issue_date": "2025-12-17", "expiry_date": "2028-12-17", "file_url": ""},
                {"name": "HCIE-Cloud", "category": "technical", "status": "active", "issue_date": "2025-05-29", "expiry_date": "2028-05-29", "file_url": ""},
            ],
            "languages": {"cantonese": "Fluent", "english": "Fluent", "mandarin": "Native"},
            "fans_count": 38,
            "welink_id": "60049788",
        },
        {
            "name": "Marcus Ng",
            "avatar_seed": "Marcus",
            "role": "TMO Engineer",
            "team": "TMO",
            "title": "Cloud Deployment Specialist",
            "bio": "Focused on AI service deployment, big data project, all aspects of cloud services development and installation",
            "skills": ["Docker", "Jenkins", "Ansible", "AI", "CodeArts", "MaaS", "Big Data", "Cloud Migration"],
            "certificates": [{"name": "Oracle Certified Professional", "category": "technical", "status": "active", "issue_date": "2023-09-15", "expiry_date": "2027-09-15", "file_url": ""}],
            "languages": {"cantonese": "N/A", "english": "Professional", "mandarin": "Native"},
            "fans_count": 25,
            "welink_id": "wx1437672",
        },
        {
            "name": "Andy Yuan",
            "avatar_seed": "Andy",
            "role": "TMO Engineer",
            "team": "TMO",
            "title": "Public Cloud TD",
            "bio": "Public Cloud TD",
            "skills": ["CCE", "Cloud Migration", "Network", "Python", "GaussDB"],
            "certificates": [
                {"name": "HCIE-Cloud", "category": "technical", "status": "active", "issue_date": "2024-07-27", "expiry_date": "2027-07-26", "file_url": ""},
                {"name": "CKA", "category": "technical", "status": "active", "issue_date": "2025-12-13", "expiry_date": "2027-12-13", "file_url": ""},
            ],
            "languages": {"cantonese": "Fluent", "english": "Fluent", "mandarin": "Native"},
            "fans_count": 67,
            "welink_id": "60093692",
            "photo_url": "/api/uploads/59dab9a820ea4c419b9702a4d49a1213.jpeg",
        },
        {
            "name": "Allen Zhong",
            "avatar_seed": "Allen",
            "role": "Techinical Director",
            "team": "TMO",
            "title": "Public Cloud TD",
            "bio": "up to 4 years experiences of cloud delivery, including Migration, Services depolyment,Stress test, Disaster Recovery Drill, Landing Zone, Security Test etc.",
            "skills": ["Landingzone", "GaussDB", "Network", "CCE", "MySQL"],
            "certificates": [
                {"name": "HCIE-Cloud", "category": "technical", "status": "active", "issue_date": "2024-12-12", "expiry_date": "2027-12-11", "file_url": ""},
                {"name": "ITIL Foundation", "category": "technical", "status": "active", "issue_date": "2026-01-06", "expiry_date": "2029-01-06", "file_url": ""},
            ],
            "languages": {"cantonese": "Fluent", "english": "Fluent", "mandarin": "Native"},
            "fans_count": 31,
            "welink_id": "84255058",
            "photo_url": "/api/uploads/d2f1a34394d54e66ae10948054414f08.png",
        },
        {
            "name": "Oliver Chang",
            "avatar_seed": "Oliver",
            "role": "TMO Engineer",
            "team": "TMO",
            "title": "Public Cloud TD",
            "bio": "Cloud security specialist with deep expertise in compliance frameworks.",
            "skills": ["WAF", "DDoS Protection", "Cloud Desktop", "Cloud Security", "Cloud Migration", "VPN", "VPC"],
            "certificates": [{"name": "HCIE-Cloud", "category": "technical", "status": "active", "issue_date": "2026-04-23", "expiry_date": "2029-04-23", "file_url": ""}],
            "languages": {"cantonese": "Basic", "english": "Professional", "mandarin": "Native"},
            "fans_count": 29,
            "welink_id": "wx1395073",
        },
        {
            "name": "TIM Zhong",
            "avatar_seed": "timzhong",
            "role": "TMO Engineer",
            "team": "TMO",
            "title": "Public Cloud TD",
            "bio": "Public Cloud TD",
            "skills": [],
            "certificates": [{"name": "HCIE-Cloud", "category": "technical", "status": "active", "issue_date": "2025-09-28", "expiry_date": "2028-09-28", "file_url": ""}],
            "languages": {"cantonese": "Native", "english": "Professional", "mandarin": "Native"},
            "fans_count": 0,
            "welink_id": "wx1437673",
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
        {
            "name": "DCI iamSmart Migration Phase 2",
            "client": "DPO",
            "description": "The \"iAM Smart\" mobile application provides a one-stop personalized digital services platform, enabling users to log in and access online services in a smarter and more convenient way using their personal mobile phones. Its English name, \"iAM Smart,\" stands for \"internet Access by Mobile in a Smart way.\" The application currently provides over 380 services to more than 3.5 million Hong Kong citizens.\n\nThis project involves migrating the \"iAM Smart\" application from the existing GCIS data center to the Huawei Base Cloud for the client, alongside undergoing an Xinchuang (Information Technology Application Innovation) transformation. Phase II of the migration entails deploying the application across the UAT, iSIT, and PROD environments.",
            "start_date": "2026-09-30",
            "end_date": "2026-10-03",
            "status": "active",
        },
        {
            "name": "传音AI migration project",
            "client": "传音",
            "description": "此次迁移传音智能机手机助手AI 业务。现网客户有三个节点覆盖全球：1 爱尔兰：使用爱尔兰节点覆盖亚非拉，目前在AWS 上，月消耗：1M USD/月，此次迁移AWS爱尔兰节点到到华为云爱尔兰，以及新加坡节点搬迁，交付周期两个半月内完成割接.",
            "start_date": "2026-04-10",
            "end_date": "2026-06-30",
            "status": "active",
        },
        {
            "name": "TD运输署AI能效提升项目",
            "client": "Transportation Department",
            "description": "一个试点AI审批自动化系统，以加快以下三个许可流程的审核过程：\n1、车辆牌照续期；\n2、粤车南下行驶（STGV）；\n3、港车北上行驶（NBT）。",
            "start_date": "2026-06-10",
            "end_date": "2026-07-30",
            "status": "active",
        },
        {
            "name": "FWD POC",
            "client": "FWD insurance",
            "description": "LandingZone POC",
            "start_date": "2026-01-02",
            "end_date": "2026-07-30",
            "status": "active",
        },
    ]

    for pd in projects_data:
        p = Project(**pd)
        db.add(p)

    db.commit()

    assignments = [
        {"member_id": 1, "project_id": 2, "busy_level": "red", "role_in_project": "TD"},
        {"member_id": 2, "project_id": 2, "busy_level": "yellow", "role_in_project": "PM"},
        {"member_id": 3, "project_id": 3, "busy_level": "green", "role_in_project": "TD"},
        {"member_id": 4, "project_id": 1, "busy_level": "red", "role_in_project": "TD"},
        {"member_id": 5, "project_id": 4, "busy_level": "yellow", "role_in_project": "PM"},
        {"member_id": 6, "project_id": 4, "busy_level": "yellow", "role_in_project": "TD"},
        {"member_id": 1, "project_id": 3, "busy_level": "yellow", "role_in_project": "Advisor"},
        {"member_id": 3, "project_id": 1, "busy_level": "yellow", "role_in_project": "CI/CD Lead"},
        {"member_id": 1, "project_id": 1, "busy_level": "yellow", "role_in_project": "TD"},
        {"member_id": 6, "project_id": 2, "busy_level": "yellow", "role_in_project": "TD"},
    ]

    for ad in assignments:
        a = ProjectAssignment(**ad)
        db.add(a)

    fan_messages = [
        {
            "member_id": 1,
            "author_name": "Client CTO",
            "content": "Zhang Wei's architecture design saved us 40% on infrastructure costs!",
            "created_at": "2026-05-10T08:30:00",
        },
        {
            "member_id": 2,
            "author_name": "Team Lead",
            "content": "Li Na keeps every milestone on track. Best PMO ever!",
            "created_at": "2026-05-12T14:20:00",
        },
        {
            "member_id": 4,
            "author_name": "VP of Sales",
            "content": "Chen Xiao's strategic vision helped us win the biggest deal this year.",
            "created_at": "2026-05-15T09:00:00",
        },
        {
            "member_id": 6,
            "author_name": "CISO",
            "content": "Zhao Mei's security audit found critical vulnerabilities before go-live.",
            "created_at": "2026-05-18T16:45:00",
        },
    ]

    for fd in fan_messages:
        fm = FanMessage(**fd)
        db.add(fm)

    # ── Seed skills from member data ──
    if not db.query(Skill).first():
        all_skills: set[tuple[str, str]] = set()
        for md in members_data:
            for s in md["skills"]:
                all_skills.add((s, derive_skill_category(s)))
        for name, cat in sorted(all_skills):
            db.add(Skill(name=name, category=cat))
        db.commit()

    # ── Seed certificate templates from member data ──
    if not db.query(CertificateTemplate).first():
        all_certs: set[tuple[str, str]] = set()
        for md in members_data:
            for c in md["certificates"]:
                all_certs.add((c["name"], c["category"]))
        for name, cat in sorted(all_certs):
            db.add(CertificateTemplate(name=name, category=cat))
        db.commit()

    db.commit()
    db.close()
