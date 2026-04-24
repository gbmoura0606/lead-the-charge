from fastapi import APIRouter

from app.services.data_service import load_matches

router = APIRouter()


@router.get("/matches")
def get_matches():
    return load_matches()
