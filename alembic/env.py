import os
import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.models import Base
from dotenv import load_dotenv

load_dotenv()

# Alembic настрйоки
config = context.config
fileConfig(config.config_file_name)

# Указываем метаданные моделей
target_metadata = Base.metadata

# Получаем подключение
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в переменных окружения!")

def run_migrations_offline():
    """Запуск миграций в offline-режиме"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Запуск миграций в online-режиме с асинхронным движком"""
    connectable = create_async_engine(DATABASE_URL, future=True)

    async def run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_migrations())

# режим работы
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()