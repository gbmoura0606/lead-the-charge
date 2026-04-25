from collections.abc import Iterable
from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, selectinload

from app.db.database import session_scope
from app.db.models import Fundamental, FundamentalNote, Note, Vod

DEFAULT_FUNDAMENTALS = [
    {'name': 'Map Awareness', 'description': 'Tracking map state and threats before committing actions.'},
    {'name': 'Positioning', 'description': 'Standing where you can pressure safely and avoid unnecessary risk.'},
    {'name': 'Mechanics', 'description': 'Execution quality in movement, ability use, and trading.'},
    {'name': 'Teamfighting', 'description': 'Role execution, target selection, and timing in grouped fights.'},
    {'name': 'Decision Making', 'description': 'Choosing the highest-value play from available options.'},
]


def to_iso(dt: datetime | None) -> str | None:
    return dt.replace(microsecond=0).isoformat() if dt else None


def serialize_vod(vod: Vod) -> dict:
    return {
        'id': vod.id,
        'title': vod.title,
        'video_path': vod.video_path,
        'session_name': vod.session_name,
        'created_at': to_iso(vod.created_at),
    }


def serialize_note(note: Note) -> dict:
    return {
        'id': note.id,
        'vod_id': note.vod_id,
        'timestamp_seconds': note.timestamp_seconds,
        'text': note.text,
        'screenshot_ref': note.screenshot_ref,
        'fundamental_ids': sorted(item.id for item in note.fundamentals),
        'created_at': to_iso(note.created_at),
    }


def serialize_fundamental(fundamental: Fundamental) -> dict:
    return {
        'id': fundamental.id,
        'name': fundamental.name,
        'description': fundamental.description,
    }


def serialize_fundamental_note(note: FundamentalNote) -> dict:
    return {
        'id': note.id,
        'fundamental_id': note.fundamental_id,
        'text': note.text,
        'created_at': to_iso(note.created_at),
    }


def ensure_default_fundamentals(db: Session) -> None:
    existing = db.scalar(select(Fundamental.id).limit(1))
    if existing:
        return
    db.add_all(Fundamental(**payload) for payload in DEFAULT_FUNDAMENTALS)


def initialize_vod_review_data() -> None:
    with session_scope() as db:
        ensure_default_fundamentals(db)


def list_fundamentals() -> list[dict]:
    with session_scope() as db:
        ensure_default_fundamentals(db)
        fundamentals = db.scalars(select(Fundamental).order_by(Fundamental.name.asc())).all()
        return [serialize_fundamental(item) for item in fundamentals]


def create_fundamental(name: str, description: str | None) -> dict:
    with session_scope() as db:
        ensure_default_fundamentals(db)
        cleaned_name = name.strip()
        existing = db.scalar(select(Fundamental).where(Fundamental.name == cleaned_name))
        if existing:
            return serialize_fundamental(existing)

        fundamental = Fundamental(name=cleaned_name, description=description)
        db.add(fundamental)
        db.flush()
        db.refresh(fundamental)
        return serialize_fundamental(fundamental)


def get_fundamental_by_id(fundamental_id: str) -> dict | None:
    with session_scope() as db:
        ensure_default_fundamentals(db)
        fundamental = db.get(Fundamental, fundamental_id)
        if not fundamental:
            return None
        return serialize_fundamental(fundamental)


def create_fundamental_note(fundamental_id: str, text: str) -> dict | None:
    with session_scope() as db:
        ensure_default_fundamentals(db)
        fundamental = db.get(Fundamental, fundamental_id)
        if not fundamental:
            return None
        note = FundamentalNote(fundamental_id=fundamental_id, text=text)
        db.add(note)
        db.flush()
        db.refresh(note)
        return serialize_fundamental_note(note)


def list_fundamental_notes(fundamental_id: str) -> list[dict] | None:
    with session_scope() as db:
        ensure_default_fundamentals(db)
        fundamental = db.get(Fundamental, fundamental_id)
        if not fundamental:
            return None
        notes = db.scalars(
            select(FundamentalNote)
            .where(FundamentalNote.fundamental_id == fundamental_id)
            .order_by(desc(FundamentalNote.created_at))
        ).all()
        return [serialize_fundamental_note(item) for item in notes]


def create_vod(title: str, video_path: str, session_name: str) -> dict:
    with session_scope() as db:
        vod = Vod(title=title, video_path=video_path, session_name=session_name)
        db.add(vod)
        db.flush()
        db.refresh(vod)
        return serialize_vod(vod)


def list_vods() -> list[dict]:
    with session_scope() as db:
        vods = db.scalars(select(Vod).order_by(desc(Vod.created_at))).all()
        return [serialize_vod(item) for item in vods]


def create_vod_note(
    vod_id: str,
    timestamp_seconds: float,
    text: str,
    screenshot_ref: str | None,
    fundamental_ids: Iterable[str],
) -> dict | None:
    with session_scope() as db:
        vod = db.get(Vod, vod_id)
        if not vod:
            return None

        unique_fundamental_ids = sorted({item for item in fundamental_ids if item})

        note = Note(
            vod_id=vod_id,
            timestamp_seconds=timestamp_seconds,
            text=text,
            screenshot_ref=screenshot_ref,
        )

        if unique_fundamental_ids:
            fundamentals = db.scalars(
                select(Fundamental).where(Fundamental.id.in_(unique_fundamental_ids))
            ).all()
            note.fundamentals = fundamentals

        db.add(note)
        db.flush()
        db.refresh(note)
        db.refresh(note, attribute_names=['fundamentals'])
        return serialize_note(note)


def list_vod_notes(vod_id: str) -> list[dict] | None:
    with session_scope() as db:
        vod = db.get(Vod, vod_id)
        if not vod:
            return None

        notes = db.scalars(
            select(Note)
            .where(Note.vod_id == vod_id)
            .options(selectinload(Note.fundamentals))
            .order_by(Note.timestamp_seconds.asc(), Note.created_at.asc())
        ).all()
        return [serialize_note(item) for item in notes]
