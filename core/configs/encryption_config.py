from pydantic import BaseModel, Field


class EncryptionConfig(BaseModel):
    """Настройки сервиса шифрования"""

    secret_key: str = Field(...)
    expires_in_hours: int = Field(
        default=10,
        le=12,  # less or equal — не больше 12
        ge=1,  # greater or equal — не меньше 1
        description="Время жизни токена в часах (макс. 12)"
    )