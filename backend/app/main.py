import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db
from app.routes.daily_logs import router as daily_logs_router
from app.routes.fundamentals import router as fundamentals_router
from app.routes.matches import router as matches_router
from app.routes.notes import router as notes_router
from app.routes.stats import router as stats_router
from app.routes.sync import router as sync_router
from app.routes.vods import router as vods_router
from app.services.vod_fundamentals_service import initialize_vod_review_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='Lead The Charge API')


@app.on_event('startup')
def startup() -> None:
    init_db()
    initialize_vod_review_data()
    logger.info('Startup complete: SQLite initialized and defaults seeded.')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
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
    logger.info('GET /health')
    return {'status': 'ok'}
