from fastapi import APIRouter

from app.services.exploration_service import basic_stats, champion_stats

router = APIRouter()


@router.get('/stats/basic')
def get_basic_stats():
    return basic_stats()


@router.get('/champions')
def get_champion_stats():
    return {'champions': champion_stats()}
