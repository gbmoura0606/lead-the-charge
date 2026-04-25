from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models.fundamental import FundamentalCreate, FundamentalNoteCreate
from app.services.data_hub_service import (
    get_fundamental_notes,
    get_fundamentals,
    save_fundamental_notes,
    save_fundamentals,
    utc_now_iso,
)

router = APIRouter()

DEFAULT_FUNDAMENTALS = [
    {'name': 'Map Awareness', 'description': 'Tracking map state and threats before committing actions.'},
    {'name': 'Positioning', 'description': 'Standing where you can pressure safely and avoid unnecessary risk.'},
    {'name': 'Mechanics', 'description': 'Execution quality in movement, ability use, and trading.'},
    {'name': 'Teamfighting', 'description': 'Role execution, target selection, and timing in grouped fights.'},
    {'name': 'Decision Making', 'description': 'Choosing the highest-value play from available options.'},
]


def ensure_defaults() -> list[dict]:
    fundamentals = get_fundamentals()
    if fundamentals:
        return fundamentals

    seeded = []
    for item in DEFAULT_FUNDAMENTALS:
        seeded.append({'id': str(uuid4()), **item})
    save_fundamentals(seeded)
    return seeded


@router.get('/fundamentals')
def list_fundamentals():
    return {'fundamentals': ensure_defaults()}


@router.post('/fundamentals')
def create_fundamental(payload: FundamentalCreate):
    fundamentals = ensure_defaults()
    fundamental = {'id': str(uuid4()), **payload.model_dump()}
    fundamentals.append(fundamental)
    save_fundamentals(fundamentals)
    return fundamental


@router.get('/fundamentals/{fundamental_id}')
def get_fundamental(fundamental_id: str):
    for fundamental in ensure_defaults():
        if fundamental.get('id') == fundamental_id:
            return fundamental
    raise HTTPException(status_code=404, detail='Fundamental not found')


@router.post('/fundamentals/{fundamental_id}/notes')
def create_fundamental_note(fundamental_id: str, payload: FundamentalNoteCreate):
    get_fundamental(fundamental_id)
    notes = get_fundamental_notes()
    note = {
        'id': str(uuid4()),
        'fundamental_id': fundamental_id,
        'text': payload.text,
        'created_at': utc_now_iso(),
    }
    notes.append(note)
    save_fundamental_notes(notes)
    return note


@router.get('/fundamentals/{fundamental_id}/notes')
def list_fundamental_notes(fundamental_id: str):
    get_fundamental(fundamental_id)
    notes = [note for note in get_fundamental_notes() if note.get('fundamental_id') == fundamental_id]
    notes.sort(key=lambda item: item.get('created_at', ''), reverse=True)
    return {'notes': notes}
