from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

class AuthSettings(BaseSettings):
    """Настройки модуля авторизации"""

    OGRN:str = Field(default="1024200708069")
    KPP:str = Field(default="420501001")
    certificate_thumbprint:str = Field(...)
    api_url: str = Field(default="http://10.3.62.2:8082/api-go/login/")

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        case_sensitive=False,
        env_file=ENV_FILE_PATH,
        extra="ignore",
    )

    @property
    def signature_string(self) -> str:
        return f"{self.OGRN}{self.KPP}"
