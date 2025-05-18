"""ФОН"""

import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.database import SessionLocal
from app.models import Video

# Путь, куда сохраняются .m3u8 файлы (локально)
HLS_DIR = "static/hls"
os.makedirs(HLS_DIR, exist_ok=True)

async def process_video_background(video_id: int, video_url: str):
    # Генерируем фейковый HLS-файл
    playlist_url = await generate_fake_hls(video_id)

    # Обновляем поле playlist_url в базе данных
    async with SessionLocal() as session:
        await update_playlist_url(session, video_id, playlist_url)

    # Тут можно добавить: логгирование, запись в Redis и т.д.
    print(f"[HLS] Сгенерирован плейлист для video_id={video_id}")


async def generate_fake_hls(video_id: int) -> str:
    filename = f"{video_id}.m3u8"
    filepath = os.path.join(HLS_DIR, filename)

    content = """#EXTM3U
                #EXT-X-VERSION:3
                #EXT-X-TARGETDURATION:10
                #EXT-X-MEDIA-SEQUENCE:0
                #EXTINF:10.0,
                segment0.ts
                #EXTINF:10.0,
                segment1.ts
                #EXTINF:10.0,
                segment2.ts
                #EXT-X-ENDLIST
                """
    with open(filepath, "w") as f:
        f.write(content)

    # Возвращаем URL до файла (в будущем может быть CDN/реальный путь)
    return f"http://localhost:8000/static/hls/{filename}"


async def update_playlist_url(db: AsyncSession, video_id: int, playlist_url: str):
    stmt = (
        update(Video)
        .where(Video.id == video_id)
        .values(playlist_url=playlist_url)
    )
    await db.execute(stmt)
    await db.commit()