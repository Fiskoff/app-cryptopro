import sys
import logging


def setup_logger(
        name: str | None = None,
        level: str = "DEBUG",
        log_format: str | None = None
) -> logging.Logger:
    """
    Настраивает и возвращает логгер с базовой конфигурацией.
    Args:
        name: Имя логгера. Если None, возвращается root logger.
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_format: Строка формата. Если None, используется значение по умолчанию.

    Returns:
        logging.Logger: Настроенный объект логгера.
    """
    if log_format is None:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(funcName)s:%(lineno)d - %(message)s"
        )

    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=getattr(logging, level.upper(), logging.INFO),
            format=log_format,
            stream=sys.stdout,
            force=True
        )

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    return logger
