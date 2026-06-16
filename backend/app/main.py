from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import members, projects, fans, uploads, auth, skills, cert_templates, admins
from app.seed import seed_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Huawei Cloud Delivery Portal", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(members.router)
app.include_router(projects.router)
app.include_router(fans.router)
app.include_router(uploads.router)
app.include_router(auth.router)
app.include_router(skills.router)
app.include_router(cert_templates.router)
app.include_router(admins.router)


@app.on_event("startup")
def startup():
    seed_data()


@app.get("/api/health")
def health():
    return {"status": "ok"}