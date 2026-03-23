from pydantic_settings import BaseSettings

from app.core.auth_config import AuthSettings


class Settings(BaseSettings):
    auth: AuthSettings = AuthSettings()


settings = Settings()