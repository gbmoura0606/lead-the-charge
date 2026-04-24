# Lead The Charge — Personal LoL Data Workspace

This project is a personal analysis workspace for League of Legends.
It focuses on collecting and exposing structured data so you can inspect patterns yourself.

## Stack
- Backend: FastAPI (Python)
- Frontend: React + Vite
- Storage: JSON files (no DB yet)

## Backend endpoints
- `GET /sync` → pull latest Riot data and persist locally
- `GET /matches` → list matches (exploration-friendly rows)
- `GET /matches/{id}` → full raw match payload
- `GET /stats/basic` → simple aggregates only
- `GET /champions` → champion usage / wins
- `POST /notes`, `GET /notes`, `GET /notes/{id}`, `PUT /notes/{id}`
- `POST /daily-logs`, `GET /daily-logs`, `GET /daily-logs/{id}`

## Riot API key setup
Set these environment variables before running backend:

```bash
export RIOT_API_KEY="your-riot-api-key"
export RIOT_GAME_NAME="wave culture"
export RIOT_TAG_LINE="EUW"
# optional defaults shown:
export RIOT_PLATFORM_REGION="euw1"
export RIOT_MATCH_REGION="europe"
export RIOT_MATCH_COUNT="20"
```

## Run backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Sync Riot data
After backend starts:

```bash
curl http://localhost:8000/sync
```

This stores data under `backend/app/storage/data/`.

## Run frontend
```bash
cd frontend
npm install
# set backend URL if needed (optional locally)
# export VITE_API_URL="http://localhost:8000"
npm run dev
```

Open `http://localhost:5173`.

## Frontend pages
- `/` Dashboard (basic stats, recent matches, champion usage, sync button)
- `/matches` match explorer with filters
- `/matches/:id` raw match detail view
- `/notes` note-taking linked to match/champion/general
- `/daily-log` daily progress logs

## Railway notes
Use two Railway services from one repo:
- backend root: `backend`
- frontend root: `frontend`

Set `VITE_API_URL` on frontend to the backend public URL.
Set `ALLOWED_ORIGINS` on backend to frontend public URL.
