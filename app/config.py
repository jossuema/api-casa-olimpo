from dotenv import load_dotenv
import os

if os.getenv("ENV") == "dev":
    load_dotenv(dotenv_path=".env")

SECRET_KEY = os.getenv("SECRET_KEY")
POSTGRES_URL = os.getenv("POSTGRES_URL")
AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
AZURE_SAS_READ = os.getenv("AZURE_SAS_READ")
AZURE_SAS_WRITE = os.getenv("AZURE_SAS_WRITE")