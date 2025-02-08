from environs import Env
from sqlalchemy.orm import declarative_base

env = Env()
env.read_env()

# Данные для подключения к PostgreSQL
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_NAME = env.str("DB_NAME")
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()