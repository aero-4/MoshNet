from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = find_dotenv()
load_dotenv(env_file)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DOMAIN: str = "0.0.0.0"
    PORT: int = 8000
    API_V1: str = "/api/v1"

    DATABASE_URI: str | None = None
    REDIS_URI: str | None = None

    VIRUS_TOTAL_API_KEY: str | None = None
    GOOGLE_SAFE_BROWSING_API_KEY: str | None = None
    YANDEX_SAFE_BROWSING_KEY: str | None = None


settings = Settings()
