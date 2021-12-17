from starlette.config import Config
from starlette.datastructures import Secret, URL

config = Config(".env")
PROJECT_NAME = "wallet-API"
VERSION = "1.0.0"
POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER_NAME = config("POSTGRES_SERVER_NAME", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)
POSTGRES_DB_HOST = config("POSTGRES_DB_HOST", cast=str)  # should match postgres docker service name
DATABASE_URL = config(
    "DATABASE_URL",
    cast=URL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_NAME}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
