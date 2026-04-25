from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models.vod import VodCreate, VodNoteCreate
from app.services.data_hub_service import (
    get_vod_notes,
    get_vods,
    save_vod_notes,
    save_vods,
    utc_now_iso,
)

router = APIRouter()


@router.post('/vod')
def create_vod(payload: VodCreate):
    vods = get_vods()
    vod = {
        'id': str(uuid4()),
        'created_at': utc_now_iso(),
        **payload.model_dump(),
    }
    vods.append(vod)
    save_vods(vods)
    return vod


@router.get('/vods')
def list_vods():
    vods = sorted(get_vods(), key=lambda item: item.get('created_at', ''), reverse=True)
    return {'vods': vods}


def _get_vod(vod_id: str):
    for vod in get_vods():
        if vod.get('id') == vod_id:
            return vod
    raise HTTPException(status_code=404, detail='VOD not found')


@router.post('/vod/{vod_id}/notes')
def create_vod_note(vod_id: str, payload: VodNoteCreate):
    _get_vod(vod_id)
    notes = get_vod_notes()
    note = {
        'id': str(uuid4()),
        'vod_id': vod_id,
        'created_at': utc_now_iso(),
        **payload.model_dump(),
    }
    notes.append(note)
    save_vod_notes(notes)
    return note


@router.get('/vod/{vod_id}/notes')
def list_vod_notes(vod_id: str):
    _get_vod(vod_id)
    notes = [note for note in get_vod_notes() if note.get('vod_id') == vod_id]
    notes.sort(key=lambda item: item.get('timestamp_seconds', 0))
    return {'notes': notes}
