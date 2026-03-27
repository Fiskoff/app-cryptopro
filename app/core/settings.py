from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.configs.auth_config import AuthSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    auth_ogrn: str = Field(default="1024200708069", alias="AUTH_OGRN")
    auth_kpp: str = Field(default="420501001", alias="AUTH_KPP")
    auth_certificate_thumbprint: str = Field(alias="AUTH_CERTIFICATE_THUMBPRINT")
    auth_api_url: str = Field(default="http://10.3.62.2:8082/api-go/login/", alias="AUTH_API_URL")

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def auth(self) -> AuthSettings:
        return AuthSettings(
            OGRN=self.auth_ogrn,
            KPP=self.auth_kpp,
            certificate_thumbprint=self.auth_certificate_thumbprint,
            api_url=self.auth_api_url,
        )

settings = Settings()