from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from core import settings


class DatabaseManager:
    """
    Менеджер подключений к асинхронной базе данных.

    Args:
        url (str): Строка подключения. Настригается в DataBaseConfig, данные берутся из env файла
        echo (bool): Возвращает логи работы базы данных. Для разработки true, для продакшене false
        pool_size (int): Максимальное число одновременных подключений
        max_overflow (int): Количество дополнительных подключений при превышении максимального
    """

    def __init__(self, url: str, echo: bool = False, pool_size: int = 5, max_overflow: int = 10):
        self.engine: AsyncEngine = create_async_engine(
            url=url, echo=echo, pool_size=pool_size, max_overflow=max_overflow
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Асинхронная фабрика сессий, реализована при помощи асинхронного генератора и асинхронного контекстного менеджера

        Returns: Объект класса AsyncSession
        """
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()


db_helper = DatabaseManager(
    settings.database.url,
    settings.database.echo,
    settings.database.pool_size,
    settings.database.max_overflow,
)
