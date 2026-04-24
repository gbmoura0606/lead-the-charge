from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models.daily_log import DailyLogCreate
from app.services.data_hub_service import get_daily_logs, save_daily_logs

router = APIRouter()


@router.get('/daily-logs')
def list_daily_logs():
    logs = sorted(get_daily_logs(), key=lambda item: item.get('date', ''), reverse=True)
    return {'dailyLogs': logs}


@router.post('/daily-logs')
def create_daily_log(payload: DailyLogCreate):
    logs = get_daily_logs()
    record = {
        'id': str(uuid4()),
        **payload.model_dump(),
    }
    logs.append(record)
    save_daily_logs(logs)
    return record


@router.get('/daily-logs/{log_id}')
def get_daily_log(log_id: str):
    for log in get_daily_logs():
        if log.get('id') == log_id:
            return log
    raise HTTPException(status_code=404, detail='Daily log not found')
