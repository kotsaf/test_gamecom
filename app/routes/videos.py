"""МАРШРУТЫ"""

from fastapi import APIRouter, BackgroundTasks, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import VideoCreate, VideoOut
from app.database import SessionLocal
from app.models import Video
from app.background import process_video_background
from app.redis_cache import get_cached_video, cache_video

router = APIRouter()

# подключение к БД
async def get_db():
    async with SessionLocal() as session:
        yield session


from fastapi import Request

"""ПУБЛИКАЦИЯ ВИДЕО"""
@router.post("/videos", response_model=VideoOut)
async def create_video(
    video_data: VideoCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # создаем видео в БД
    video = Video(title=video_data.title, url=video_data.url)
    db.add(video)
    await db.commit()
    await db.refresh(video)

    # формируем абсолютную ссылку на HLS-файл
    base_url = str(request.base_url).rstrip("/")
    video.playlist_url = f"{base_url}/static/hls/{video.id}.m3u8"

    # заранее кэшируем ответ с ссылкой 
    await cache_video(video.id, video)

    # добавляем фоновую задачу
    background_tasks.add_task(
        process_video_background, video.id, video.url
    )

    return video

"""ПОЛУЧЕНИЕ ВИДЕО"""
@router.get("/videos/{video_id}", response_model=VideoOut)
async def get_video(video_id: int, db: AsyncSession = Depends(get_db)):
    # достаем из кэша
    cached = await get_cached_video(video_id)
    if cached:
        return cached

    # если нет там — из БД
    video = await db.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Видео не найдено")

    # кэшируем на будущее
    await cache_video(video_id, video)

    return video