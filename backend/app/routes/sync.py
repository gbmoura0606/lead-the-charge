from fastapi import APIRouter

from app.services.sync_service import SyncService

router = APIRouter()


@router.get('/sync')
def sync_matches():
    return SyncService().sync()
