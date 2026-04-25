from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String, Table, Text, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


note_fundamentals = Table(
    'note_fundamentals',
    Base.metadata,
    Column('note_id', String, ForeignKey('notes.id', ondelete='CASCADE'), primary_key=True),
    Column('fundamental_id', String, ForeignKey('fundamentals.id', ondelete='CASCADE'), primary_key=True),
)


class Vod(Base):
    __tablename__ = 'vods'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String, nullable=False)
    video_path: Mapped[str] = mapped_column(String, nullable=False)
    session_name: Mapped[str] = mapped_column(String, nullable=False, default='Default Session')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    notes: Mapped[list['Note']] = relationship('Note', back_populates='vod', cascade='all, delete-orphan')


class Fundamental(Base):
    __tablename__ = 'fundamentals'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    notes: Mapped[list['Note']] = relationship('Note', secondary=note_fundamentals, back_populates='fundamentals')
    brainstorm_notes: Mapped[list['FundamentalNote']] = relationship(
        'FundamentalNote',
        back_populates='fundamental',
        cascade='all, delete-orphan',
    )


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    vod_id: Mapped[str] = mapped_column(String, ForeignKey('vods.id'), nullable=False, index=True)
    timestamp_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    screenshot_ref: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    vod: Mapped[Vod] = relationship('Vod', back_populates='notes')
    fundamentals: Mapped[list[Fundamental]] = relationship('Fundamental', secondary=note_fundamentals, back_populates='notes')


class FundamentalNote(Base):
    __tablename__ = 'fundamental_notes'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    fundamental_id: Mapped[str] = mapped_column(String, ForeignKey('fundamentals.id'), nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    fundamental: Mapped[Fundamental] = relationship('Fundamental', back_populates='brainstorm_notes')
