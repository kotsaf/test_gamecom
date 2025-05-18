"""PYDANTIC СХЕМЫ"""

from pydantic import BaseModel
from typing import Optional

# схема — для POST
class VideoCreate(BaseModel):
    title: str
    url: str  # авто валидация URL

# ответ при получении или создании видео
class VideoOut(BaseModel):
    id: int
    title: str
    playlist_url: Optional[str]  # None, если пока не сгенерирован

    class Config:
        from_attributes = True  # позволяет использовать SQLAlchemy-объекты