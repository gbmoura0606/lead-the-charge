from fastapi import APIRouter

from app.services.data_service import load_matches
from app.services.stats_service import calculate_stats

router = APIRouter()


@router.get("/stats")
def get_stats():
    matches = load_matches()
    return calculate_stats(matches)
