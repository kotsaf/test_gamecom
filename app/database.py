"""РАБОТА С БД"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# создаём асинк движок sqlalchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# фабрика сессий
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# базовый класс моделей
Base = declarative_base()