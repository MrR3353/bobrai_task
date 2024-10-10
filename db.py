import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import RequestLog, Base
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, CACHE_DURATION_MINUTES

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def log_request(user_id, command, response, icon_url):
    db = SessionLocal()
    log = RequestLog(user_id=user_id, command=command, response=response, icon_url=icon_url)
    db.add(log)
    db.commit()
    db.close()


def get_cached_log(command):
    db = SessionLocal()
    log = (db.query(RequestLog).filter(RequestLog.command == command).
           filter(RequestLog.timestamp + datetime.timedelta(minutes=CACHE_DURATION_MINUTES) > datetime.datetime.utcnow()).
           order_by(RequestLog.timestamp.desc()).first())
    return log
