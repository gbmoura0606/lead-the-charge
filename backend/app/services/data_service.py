import json
from pathlib import Path

from app.models.match import Match

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "matches.json"


def load_matches() -> list[Match]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)
    return [Match(**item) for item in raw_data]
