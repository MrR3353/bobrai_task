from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    command = Column(String(50))
    response = Column(String(200))
    icon_url = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
