from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    match_id: str | None = None
    champion: str | None = None
    scope: str = "general"


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: str
    date: str
