Video API — FastAPI + PostgreSQL + Redis

Этот проект — REST API-сервис для загрузки и обработки видео, реализованный на FastAPI. Он включает асинхронную работу с PostgreSQL, кэширование с помощью Redis и обработку видео в фоне.

## Используемые технологии

- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Redis
- Alembic (миграции)
- Docker / Docker Compose
- Pydantic

---

## Как запустить проект локально

> Убедитесь, что у вас установлены Docker и Docker Compose.

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Создайте .env файл
Создайте .env в корне проекта:

DATABASE_URL=postgresql+asyncpg://safar:safar@db:5432/game_test
REDIS_URL=redis://redis:6379
Также можно скопировать из примера:

cp .env.example .env
3. Запустите проект с помощью Docker Compose
docker compose up --build
Это поднимет следующие сервисы:

app — FastAPI-приложение
db — PostgreSQL
redis — Redis
Приложение будет доступно на:
http://localhost:8000

4. Примените миграции
!!После запуска, в новом терминале выполните:

docker compose exec app alembic upgrade head
Это создаст таблицы в базе данных.

5. Используйте API
Документация Swagger будет доступна по адресу:

http://localhost:8000/docs
Там вы можете:

загружать видео (POST /api/videos)
получать видео по ID (GET /api/videos/{id})
Структура проекта

.
├── alembic/                   # Миграции
│   └── versions/
├── app/
│   ├── main.py                # Точка входа
│   ├── database.py            # Подключение к БД
│   ├── backround.py           # Фон
│   ├── models.py              # SQLAlchemy модели
│   ├── redis_cache.py         # Кэширование
│   ├── schemas.py             # Pydantic сземы
│   └── routes/
│       └── videos.py          # Роуты
├── Dockerfile
├── docker-compose.yml
├── alembic.ini                # Настройки алембик
├── .env                       # Переменные окружения
├── requirements.txt           # Зависимости
└── .gitignore

Примечания

Все переменные конфигурации находятся в .env
База данных и Redis запускаются внутри Docker контейнеров
Видео обрабатываются асинхронно в фоне (фейковая обработка HLS)
