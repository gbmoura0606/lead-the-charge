import logging

from fastapi import APIRouter, HTTPException

from app.services.exploration_service import get_match_detail, list_matches

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/matches')
def get_matches():
    logger.info('GET /matches')
    return {'matches': list_matches()}


@router.get('/matches/{match_id}')
def get_match(match_id: str):
    logger.info('GET /matches/%s', match_id)
    match = get_match_detail(match_id)
    if not match:
        raise HTTPException(status_code=404, detail='Match not found')
    return match
