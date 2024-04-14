from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL")
APP_TOKEN = os.getenv("APP_TOKEN", "")
