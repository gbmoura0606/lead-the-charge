# Lead The Charge (v0)

League of Legends performance dashboard for a single-user improvement workflow.

## Stack
- Frontend: React + Vite
- Backend: FastAPI
- Storage: JSON file (for now)

## Run backend (local)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run frontend (local)
```bash
cd frontend
npm install
npm run dev
```

The frontend expects backend on `http://localhost:8000`.

## API endpoints
- `GET /matches`
- `GET /stats`
- `GET /insights`
- `GET /health`

## Quick test flow
1. Start backend and frontend.
2. Open `http://localhost:5173`.
3. Confirm summary cards, champion/role performance, and insight list are visible.
4. Optional API checks:
   - `curl http://localhost:8000/stats`
   - `curl http://localhost:8000/insights`

## Railway deployment (public URLs)
Create **2 Railway services** from the same repo (monorepo setup):

### Service 1: backend-api
- Root directory: `backend`
- Build command:
  ```bash
  pip install -r requirements.txt
  ```
- Start command:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- Environment variables:
  - `ALLOWED_ORIGINS=https://<your-frontend-domain>.up.railway.app`

### Service 2: frontend-web
- Root directory: `frontend`
- Build command:
  ```bash
  npm install && npm run build
  ```
- Start command:
  ```bash
  npm run preview
  ```
- Environment variables:
  - `VITE_API_URL=https://<your-backend-domain>.up.railway.app`
  - `VITE_ALLOWED_HOST=<your-frontend-domain>.up.railway.app` (optional, for custom preview host allow-list)

After both are deployed:
1. Copy backend public URL into frontend `VITE_API_URL` and redeploy frontend.
2. Copy frontend public URL into backend `ALLOWED_ORIGINS` and redeploy backend.

## Railway readiness notes
- Backend is stateless aside from JSON file read.
- API layer is separated from service logic for easier DB migration.
- Configure CORS and `VITE_API_URL` in deployment environments.
