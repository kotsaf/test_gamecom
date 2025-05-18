"""ТОЧКА ВХОДА"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import videos

app = FastAPI(
    title="Video Streaming API",
    description="Сервис управления видеопотоками (FastAPI + HLS + Redis)",
    version="1.0.0",
)

# подключаем роуты
app.include_router(videos.router, prefix="/api", tags=["Videos"])

# подключаем статику (.m3u8 и .ts)
app.mount("/static", StaticFiles(directory="static"), name="static")