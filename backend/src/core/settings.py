from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

env_file = find_dotenv()
load_dotenv(env_file)


class Settings(BaseSettings):
    DOMAIN: str = "0.0.0.0"
    PORT: int = 8000
    API_V1: str = "/api/v1"

    DATABASE_URI: str | None = None
    REDIS_URI: str | None = None

    VIRUS_TOTAL_API_KEY: str | None = None
    GOOGLE_SAFE_BROWSING_API_KEY: str | None = None

settings = Settings()
