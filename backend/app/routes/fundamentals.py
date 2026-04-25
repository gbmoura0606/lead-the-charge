import logging

from fastapi import APIRouter, HTTPException

from app.models.fundamental import FundamentalCreate, FundamentalNoteCreate
from app.services.vod_fundamentals_service import (
    create_fundamental,
    create_fundamental_note,
    get_fundamental_by_id,
    list_fundamental_notes,
    list_fundamentals,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/fundamentals')
def get_fundamentals():
    logger.info('GET /fundamentals')
    return {'fundamentals': list_fundamentals()}


@router.post('/fundamentals')
def post_fundamental(payload: FundamentalCreate):
    logger.info('POST /fundamentals')
    return create_fundamental(payload.name, payload.description)


@router.get('/fundamentals/{fundamental_id}')
def get_fundamental(fundamental_id: str):
    logger.info('GET /fundamentals/%s', fundamental_id)
    fundamental = get_fundamental_by_id(fundamental_id)
    if not fundamental:
        raise HTTPException(status_code=404, detail='Fundamental not found')
    return fundamental


@router.post('/fundamentals/{fundamental_id}/notes')
def post_fundamental_note(fundamental_id: str, payload: FundamentalNoteCreate):
    logger.info('POST /fundamentals/%s/notes', fundamental_id)
    note = create_fundamental_note(fundamental_id, payload.text)
    if not note:
        raise HTTPException(status_code=404, detail='Fundamental not found')
    return note


@router.get('/fundamentals/{fundamental_id}/notes')
def get_fundamental_notes(fundamental_id: str):
    logger.info('GET /fundamentals/%s/notes', fundamental_id)
    notes = list_fundamental_notes(fundamental_id)
    if notes is None:
        raise HTTPException(status_code=404, detail='Fundamental not found')
    return {'notes': notes}
