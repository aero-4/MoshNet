from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _env_files() -> tuple[str, ...]:
    app_dir = Path(__file__).resolve().parents[2]
    project_dir = app_dir.parent
    candidates = (
        project_dir / ".env",
        app_dir / ".env",
        Path("/app/.env"),
    )

    env_files: list[str] = []
    seen: set[Path] = set()
    for candidate in candidates:
        path = candidate.resolve()
        if path in seen or not path.is_file():
            continue

        env_files.append(str(path))
        seen.add(path)

    return tuple(env_files)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_files(),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
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
