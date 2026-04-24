from fastapi import APIRouter

from app.services.data_service import load_matches
from app.services.insights_service import generate_insights

router = APIRouter()


@router.get("/insights")
def get_insights():
    matches = load_matches()
    return {"insights": generate_insights(matches)}
