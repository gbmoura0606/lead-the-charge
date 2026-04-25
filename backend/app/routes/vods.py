import logging

from fastapi import APIRouter, HTTPException

from app.models.vod import VodCreate, VodNoteCreate
from app.services.vod_fundamentals_service import (
    create_vod,
    create_vod_note,
    list_vod_notes,
    list_vods,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/vod')
def post_vod(payload: VodCreate):
    logger.info('POST /vod')
    return create_vod(payload.title, payload.video_path, payload.session_name)


@router.get('/vods')
def get_vods():
    logger.info('GET /vods')
    return {'vods': list_vods()}


@router.post('/vod/{vod_id}/notes')
def post_vod_note(vod_id: str, payload: VodNoteCreate):
    logger.info('POST /vod/%s/notes', vod_id)
    note = create_vod_note(
        vod_id=vod_id,
        timestamp_seconds=payload.timestamp_seconds,
        text=payload.text,
        screenshot_ref=payload.screenshot_ref,
        fundamental_ids=payload.fundamental_ids,
    )
    if not note:
        raise HTTPException(status_code=404, detail='VOD not found')
    return note


@router.get('/vod/{vod_id}/notes')
def get_vod_notes(vod_id: str):
    logger.info('GET /vod/%s/notes', vod_id)
    notes = list_vod_notes(vod_id)
    if notes is None:
        raise HTTPException(status_code=404, detail='VOD not found')
    return {'notes': notes}
