from fastapi import APIRouter, HTTPException

from app.services.exploration_service import get_match_detail, list_matches

router = APIRouter()


@router.get('/matches')
def get_matches():
    return {'matches': list_matches()}


@router.get('/matches/{match_id}')
def get_match(match_id: str):
    match = get_match_detail(match_id)
    if not match:
        raise HTTPException(status_code=404, detail='Match not found')
    return match
