from aiogram import Bot, Dispatcher

from src.config.config import CONN_DB, TG_TOKEN
from src.database.postgres_manager import PostgresManager

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

pg_manager = PostgresManager(CONN_DB)
