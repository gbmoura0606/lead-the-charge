from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.storage.json_store import JsonStore

DATA_DIR = Path(__file__).resolve().parent.parent / "storage" / "data"
SUMMONER_FILE = DATA_DIR / "summoner.json"
MATCHES_FILE = DATA_DIR / "matches.json"
NOTES_FILE = DATA_DIR / "notes.json"
DAILY_LOGS_FILE = DATA_DIR / "daily_logs.json"
VODS_FILE = DATA_DIR / "vods.json"
VOD_NOTES_FILE = DATA_DIR / "vod_notes.json"
FUNDAMENTALS_FILE = DATA_DIR / "fundamentals.json"
FUNDAMENTAL_NOTES_FILE = DATA_DIR / "fundamental_notes.json"

summoner_store = JsonStore(SUMMONER_FILE, default={})
matches_store = JsonStore(MATCHES_FILE, default=[])
notes_store = JsonStore(NOTES_FILE, default=[])
daily_logs_store = JsonStore(DAILY_LOGS_FILE, default=[])
vods_store = JsonStore(VODS_FILE, default=[])
vod_notes_store = JsonStore(VOD_NOTES_FILE, default=[])
fundamentals_store = JsonStore(FUNDAMENTALS_FILE, default=[])
fundamental_notes_store = JsonStore(FUNDAMENTAL_NOTES_FILE, default=[])


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


def get_vods() -> list[dict[str, Any]]:
    return vods_store.read()


def save_vods(vods: list[dict[str, Any]]) -> None:
    vods_store.write(vods)


def get_vod_notes() -> list[dict[str, Any]]:
    return vod_notes_store.read()


def save_vod_notes(notes: list[dict[str, Any]]) -> None:
    vod_notes_store.write(notes)


def get_fundamentals() -> list[dict[str, Any]]:
    return fundamentals_store.read()


def save_fundamentals(fundamentals: list[dict[str, Any]]) -> None:
    fundamentals_store.write(fundamentals)


def get_fundamental_notes() -> list[dict[str, Any]]:
    return fundamental_notes_store.read()


def save_fundamental_notes(notes: list[dict[str, Any]]) -> None:
    fundamental_notes_store.write(notes)
