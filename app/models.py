"""МОДЕЛЬ БД"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Video(Base):
    # название таблицы
    __tablename__ = 'videos'

    # колонки
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    playlist_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)