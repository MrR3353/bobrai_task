from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import RequestLog

app = FastAPI(
    title="Telegram Weather Bot API",
    description="API для работы с Telegram-ботом и просмотра истории запросов.",
    version="1.0.0",
)


@app.get("/logs", summary="Получение истории запросов")
def get_logs(start_date: datetime = None, end_date: datetime = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(RequestLog)
    if start_date:
        query = query.filter(RequestLog.timestamp >= start_date)
    if end_date:
        query = query.filter(RequestLog.timestamp <= end_date)
    return query.offset(skip).limit(limit).all()


@app.get("/logs/{user_id}", summary="Получение логов пользователя")
def get_logs_by_user(user_id: int, start_date: datetime = None, end_date: datetime = None,
                     db: Session = Depends(get_db)):
    query = db.query(RequestLog).filter(RequestLog.user_id == user_id)
    if start_date:
        query = query.filter(RequestLog.timestamp >= start_date)
    if end_date:
        query = query.filter(RequestLog.timestamp <= end_date)
    return query.all()
