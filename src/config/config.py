import os

import dotenv
from loguru import logger

try:
    dotenv.load_dotenv(dotenv_path=".env")
except Exception as exception:
    logger.error("Failed to load .env file: %s", exception)
finally:
    if not os.getenv("POSTGRES_DB"):
        logger.error("POSTGRES_DB is not set")
    if not os.getenv("POSTGRES_USER"):
        logger.error("POSTGRES_USER is not set")
    if not os.getenv("POSTGRES_PASSWORD"):
        logger.error("POSTGRES_PASSWORD is not set")
    if not os.getenv("POSTGRES_DB"):
        logger.error("POSTGRES_DB is not set")
    if not os.getenv("TG_TOKEN"):
        logger.error("TG_TOKEN is not set")
    if not os.getenv("CHAT_ID"):
        logger.error("CHAT_ID is not set")


POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CONN_DB = {
    "host": POSTGRES_HOST,
    "database": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
}
