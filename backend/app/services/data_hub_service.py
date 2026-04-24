from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.storage.json_store import JsonStore

DATA_DIR = Path(__file__).resolve().parent.parent / "storage" / "data"
SUMMONER_FILE = DATA_DIR / "summoner.json"
MATCHES_FILE = DATA_DIR / "matches.json"
NOTES_FILE = DATA_DIR / "notes.json"
DAILY_LOGS_FILE = DATA_DIR / "daily_logs.json"

summoner_store = JsonStore(SUMMONER_FILE, default={})
matches_store = JsonStore(MATCHES_FILE, default=[])
notes_store = JsonStore(NOTES_FILE, default=[])
daily_logs_store = JsonStore(DAILY_LOGS_FILE, default=[])


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_summoner() -> dict[str, Any]:
    return summoner_store.read()


def save_summoner(summoner: dict[str, Any]) -> None:
    payload = {
        "synced_at": utc_now_iso(),
        "data": summoner,
    }
    summoner_store.write(payload)


def get_matches() -> list[dict[str, Any]]:
    return matches_store.read()


def save_matches(matches: list[dict[str, Any]]) -> None:
    matches_store.write(matches)


def upsert_match(match: dict[str, Any]) -> None:
    matches = get_matches()
    match_id = match.get("metadata", {}).get("matchId")
    if not match_id:
        return

    by_id = {item.get("metadata", {}).get("matchId"): item for item in matches}
    by_id[match_id] = match
    save_matches(list(by_id.values()))


def get_notes() -> list[dict[str, Any]]:
    return notes_store.read()


def save_notes(notes: list[dict[str, Any]]) -> None:
    notes_store.write(notes)


def get_daily_logs() -> list[dict[str, Any]]:
    return daily_logs_store.read()


def save_daily_logs(logs: list[dict[str, Any]]) -> None:
    daily_logs_store.write(logs)
