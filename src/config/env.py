"""parse .env variables"""
import os

from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")

POSTGRES_CONNECT = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
)
