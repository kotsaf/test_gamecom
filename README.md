# Video API — FastAPI + PostgreSQL + Redis

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

### Как запустить проект локально

> У вас должны быть установлены Docker и Docker Compose.


## 1. Клонируйте репозиторий
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
## 2. Создайте .env файл
Создайте .env в корне проекта c:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/db_name
REDIS_URL=redis://redis:6379
```

## 3. Запустите проект с помощью Docker Compose
```bash
docker compose up --build
```
Это поднимет следующие сервисы:

app — FastAPI-приложение<br>
db — PostgreSQL<br>
redis — Redis<br><br>
Приложение будет доступно на:
http://localhost:8000

## 4. Примените миграции
!!После запуска, в новом терминале выполните:
```bash
docker compose exec app alembic upgrade head
```
Это создаст таблицы в базе данных.

## 5. Используйте API
Документация Swagger будет доступна по адресу:

http://localhost:8000/docs <br>
Там вы можете:
- загружать видео (POST /api/videos)
- получать видео по ID (GET /api/videos/{id})


## Структура проекта
```bash
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
```

Примечания

- Все переменные конфигурации находятся в .env
- База данных и Redis запускаются внутри Docker контейнеров
- Видео обрабатываются асинхронно в фоне
