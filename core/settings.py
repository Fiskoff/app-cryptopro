from pydantic_settings import BaseSettings

from core.auth_config import AuthSettings


class Settings(BaseSettings):
    auth: AuthSettings = AuthSettings()


settings = Settings()