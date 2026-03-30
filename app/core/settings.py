from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.configs.auth_config import AuthConfig
from app.core.configs.database_config import DataBaseConfig


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Глобальные настройки проекта. Единственный класс, который читает .env"""

    auth: AuthConfig = Field(default_factory=AuthConfig)
    database: DataBaseConfig = Field(default_factory=DataBaseConfig)

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
        env_nested_delimiter="__",
    )


settings = Settings()