from typing import Protocol, Optional


class ITokenRepository(Protocol):
    """Контракт для репозитория токенов."""

    async def create_token(self, token: str, expires_in_hours: int) -> object:
        """Создаёт зашифрованный токен с заданным временем жизни."""
        ...

    async def get_by_token(self, token: str) -> Optional[object]:
        """Получает запись токена по сырому значению (без проверки валидности)."""
        ...

    async def get_valid_token(self, token: str) -> Optional[object]:
        """Получает только валидный (не истёкший и не отозванный) токен."""
        ...