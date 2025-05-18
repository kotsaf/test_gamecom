"""РАБОТА С РЕДИС (КЕШ)"""

import os
import json
from dotenv import load_dotenv
from app.schemas import VideoOut
import redis.asyncio as redis

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL = 60 * 5  # 5 минут

# Redis клиент асинхронный
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def cache_video(video_id: int, video_obj):
    data = {
        "id": video_obj.id,
        "title": video_obj.title,
        "playlist_url": video_obj.playlist_url,
    }
    await redis_client.set(f"video:{video_id}", json.dumps(data), ex=CACHE_TTL)

async def get_cached_video(video_id: int):
    data = await redis_client.get(f"video:{video_id}")
    if data:
        return VideoOut(**json.loads(data))
    return None