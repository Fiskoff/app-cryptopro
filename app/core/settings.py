from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.auth_config import AuthSettings  # Прямой импорт!


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Настройки всего проекта"""
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra="ignore",
    )

    @property
    def auth(self) -> AuthSettings:
        return AuthSettings()


settings = Settings()