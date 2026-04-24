from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models.note import NoteCreate
from app.services.data_hub_service import get_notes, save_notes, utc_now_iso

router = APIRouter()


@router.get('/notes')
def list_notes():
    notes = sorted(get_notes(), key=lambda item: item.get('date', ''), reverse=True)
    return {'notes': notes}


@router.get('/notes/{note_id}')
def get_note(note_id: str):
    for note in get_notes():
        if note.get('id') == note_id:
            return note
    raise HTTPException(status_code=404, detail='Note not found')


@router.post('/notes')
def create_note(payload: NoteCreate):
    notes = get_notes()
    note = {
        'id': str(uuid4()),
        'date': utc_now_iso(),
        **payload.model_dump(),
    }
    notes.append(note)
    save_notes(notes)
    return note


@router.put('/notes/{note_id}')
def update_note(note_id: str, payload: NoteCreate):
    notes = get_notes()
    for index, note in enumerate(notes):
        if note.get('id') == note_id:
            updated = {
                **note,
                **payload.model_dump(),
            }
            notes[index] = updated
            save_notes(notes)
            return updated

    raise HTTPException(status_code=404, detail='Note not found')
