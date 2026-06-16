"""
导出当前数据库内容 → seed.py 格式。

用法：
  方式1（Docker)： docker exec -it portal-backend python dump_seed.py
  方式2（本地）：  cd backend && python dump_seed.py

输出可直接替换 seed.py 中的硬编码数据。
"""
import json
import os
import sys

# ensure we can import app modules
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models import Member, Project, ProjectAssignment, FanMessage


def dump():
    db = SessionLocal()

    # ── Members ──
    members = db.query(Member).all()
    members_data = []
    for m in members:
        members_data.append({
            "name": m.name,
            "avatar_seed": m.avatar_seed,
            "role": m.role,
            "team": m.team,
            "title": m.title,
            "bio": m.bio,
            "welink_id": m.welink_id or "",
            "photo_url": m.photo_url or "",
            "skills": json.loads(m.skills) if isinstance(m.skills, str) else m.skills,
            "certificates": json.loads(m.certificates) if isinstance(m.certificates, str) else m.certificates,
            "languages": json.loads(m.languages) if isinstance(m.languages, str) else m.languages,
            "fans_count": m.fans_count,
        })

    # ── Projects ──
    projects = db.query(Project).all()
    projects_data = []
    for p in projects:
        projects_data.append({
            "name": p.name,
            "client": p.client,
            "description": p.description,
            "start_date": p.start_date,
            "end_date": p.end_date,
            "status": p.status,
        })

    # ── Assignments (use member_id / project_id, NOT auto-increment id) ──
    assignments = db.query(ProjectAssignment).all()
    assignments_data = []
    for a in assignments:
        assignments_data.append({
            "member_id": a.member_id,
            "project_id": a.project_id,
            "busy_level": a.busy_level,
            "role_in_project": a.role_in_project,
        })

    # ── Fan Messages ──
    fan_messages = db.query(FanMessage).all()
    fan_messages_data = []
    for f in fan_messages:
        fan_messages_data.append({
            "member_id": f.member_id,
            "author_name": f.author_name,
            "content": f.content,
            "created_at": f.created_at,
        })

    db.close()

    # ── Render as Python code ──
    print("=" * 50)
    print("# 复制以下内容替换 seed.py 中的 seed_data() 函数体")
    print("=" * 50)
    print()

    default_lang = {"cantonese": "N/A", "english": "N/A", "mandarin": "N/A"}

    # Render with pretty-print
    for i, md in enumerate(members_data):
        # Keep languages compact (single line)
        lang_pretty = json.dumps(md["languages"], ensure_ascii=False, separators=(", ", ": "))
        skills_pretty = json.dumps(md["skills"], ensure_ascii=False)
        certs_pretty = json.dumps(md["certificates"], ensure_ascii=False)

        print(f"        {{")
        print(f'            "name": {json.dumps(md["name"], ensure_ascii=False)},')
        print(f'            "avatar_seed": {json.dumps(md["avatar_seed"], ensure_ascii=False)},')
        print(f'            "role": {json.dumps(md["role"], ensure_ascii=False)},')
        print(f'            "team": {json.dumps(md["team"], ensure_ascii=False)},')
        print(f'            "title": {json.dumps(md["title"], ensure_ascii=False)},')
        print(f'            "bio": {json.dumps(md["bio"], ensure_ascii=False)},')
        print(f'            "skills": {skills_pretty},')
        print(f'            "certificates": {certs_pretty},')
        print(f'            "languages": {lang_pretty},')
        print(f'            "fans_count": {md["fans_count"]},')
        print(f'            "welink_id": {json.dumps(md["welink_id"], ensure_ascii=False)},')
        if md.get("photo_url"):
            print(f'            "photo_url": {json.dumps(md["photo_url"], ensure_ascii=False)},')
        print(f"        }},")
        print()

    print("    # --- Projects ---")
    for pd_item in projects_data:
        print(f"        {{")
        for k, v in pd_item.items():
            print(f'            "{k}": {json.dumps(v, ensure_ascii=False)},')
        print(f"        }},")
        print()

    print("    # --- Assignments ---")
    for ad in assignments_data:
        print(f"        {{")
        for k, v in ad.items():
            print(f'            "{k}": {json.dumps(v, ensure_ascii=False)},')
        print(f"        }},")
        print()

    print("    # --- Fan Messages ---")
    for fd in fan_messages_data:
        print(f"        {{")
        for k, v in fd.items():
            print(f'            "{k}": {json.dumps(v, ensure_ascii=False)},')
        print(f"        }},")
        print()


if __name__ == "__main__":
    dump()
