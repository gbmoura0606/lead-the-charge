import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.insights import router as insights_router
from app.routes.matches import router as matches_router
from app.routes.stats import router as stats_router

app = FastAPI(title="Lead The Charge API")

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matches_router)
app.include_router(stats_router)
app.include_router(insights_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
