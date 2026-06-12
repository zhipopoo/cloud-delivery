# Huawei Cloud Delivery Portal

Internal management dashboard for the **Huawei Public Cloud Delivery Team**.

## Architecture

| Layer | Stack |
|-------|-------|
| Frontend | Vue 3 + Vite + TypeScript + Tailwind CSS + Ant Design Vue |
| Backend | FastAPI + SQLAlchemy + SQLite |
| Deployment | Docker + Docker Compose |

## Quick Start (Docker)

```bash
docker-compose up --build
```

| Service | URL |
|----------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

## Local Development

### Prerequisites

- **Node.js** ≥ 18
- **Python** ≥ 3.10
- **Docker** (optional, for containerized deployment)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The API server starts at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server starts at `http://localhost:5173` with HMR enabled.

### Build for Production

```bash
# Frontend
cd frontend
npm run build        # outputs to frontend/dist/

# Backend (no build step needed — just run via Docker or directly)
```

## Project Structure

```
cloud-delivery/
├── frontend/                # Vue 3 SPA
│   ├── src/
│   │   ├── api/             # Axios API clients
│   │   ├── assets/          # Static assets
│   │   ├── components/      # Reusable Vue components
│   │   ├── router/          # Vue Router config
│   │   ├── stores/          # Pinia stores
│   │   ├── types/           # TypeScript type definitions
│   │   └── views/           # Page-level components
│   ├── Dockerfile
│   └── nginx.conf
├── backend/                 # FastAPI service
│   ├── app/
│   │   ├── routers/         # API route modules
│   │   ├── main.py          # App entry point
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── database.py      # DB connection setup
│   │   └── seed.py          # Seed data
│   ├── run.py               # Server launcher
│   └── Dockerfile
└── docker-compose.yml       # Multi-service orchestration
```

## Core Modules

| Module | Description |
|--------|-------------|
| Team | Tree-filtered team view (TMO / PMO / Management) with profile cards |
| Skills | Skill matrix with member linkage and category grouping |
| Certificates | Technical & general certs with status indicators |
| Languages | Cantonese / English / Mandarin proficiency matrix with progress bars |
| Fans | Social module — peer messages, fan count leaderboard |
| Calendar | Project resource timeline with busy-level color coding (red/yellow/green) |

## Design System

| Token | Value |
|-------|-------|
| Primary | `#007DFF` (Huawei Blue) |
| Accent | `#00C9FF` (Cyan) |
| Theme | Dark mode with geometric hex patterns, floating depth elements, glassmorphism cards |
| Avatars | DiceBear Bottts (game-style avatars seeded by name) |