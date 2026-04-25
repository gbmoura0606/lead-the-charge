import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.daily_logs import router as daily_logs_router
from app.routes.matches import router as matches_router
from app.routes.notes import router as notes_router
from app.routes.stats import router as stats_router
from app.routes.vods import router as vods_router
from app.routes.fundamentals import router as fundamentals_router
from app.routes.sync import router as sync_router

app = FastAPI(title='Lead The Charge API')

allowed_origins_env = os.getenv('ALLOWED_ORIGINS', '').strip()
if allowed_origins_env:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(',') if origin.strip()]
    allow_credentials = True
else:
    allowed_origins = ['*']
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(sync_router)
app.include_router(matches_router)
app.include_router(stats_router)
app.include_router(notes_router)
app.include_router(daily_logs_router)
app.include_router(vods_router)
app.include_router(fundamentals_router)


@app.get('/health')
def health_check():
    return {'status': 'ok'}
