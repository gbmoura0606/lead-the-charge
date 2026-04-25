from pydantic import BaseModel


class FundamentalCreate(BaseModel):
    name: str
    description: str | None = None


class FundamentalNoteCreate(BaseModel):
    text: str
