import logging
import sys

from app.core.configs.logger_config import LoggerConfig


class LoggerManager:
    """Менеджер настройки логгера"""

    @staticmethod
    def setup(config: LoggerConfig | None = None, **kwargs) -> logging.Logger:
        """
        Настраивает логгер и возвращает готовый экземпляр.

        Args:
            config: Объект LoggerConfig (опционально)
            **kwargs: Прямые параметры: name, level, format (перебивают конфиг)

        Returns:
            logging.Logger: Настроенный логгер
        """

        name = kwargs.get("name") or (config.name if config else None)
        level = kwargs.get("level") or (config.level if config else "INFO")
        fmt = kwargs.get("format") or (config.format if config else None)

        if fmt is None:
            fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        logging.basicConfig(
            level=getattr(logging, level.upper(), logging.INFO),
            format=fmt,
            stream=sys.stdout,
            force=True,
        )

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        return logger

    @staticmethod
    def quick(name: str | None = None, level: str = "INFO") -> logging.Logger:
        """Быстрый способ получить логгер без создания конфига."""
        
        return LoggerManager.setup(name=name, level=level)