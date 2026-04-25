from pydantic import BaseModel, Field


class VodCreate(BaseModel):
    title: str
    video_path: str
    session_name: str = 'Default Session'


class VodNoteCreate(BaseModel):
    timestamp_seconds: float = Field(ge=0)
    text: str
    fundamental_ids: list[str] = Field(default_factory=list)
    screenshot_ref: str | None = None
