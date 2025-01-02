from dotenv import load_dotenv
import os

if os.getenv("ENV") == "dev":
    load_dotenv(dotenv_path=".env")

SECRET_KEY = os.getenv("SECRET_KEY")
POSTGRES_URL = os.getenv("POSTGRES_URL")