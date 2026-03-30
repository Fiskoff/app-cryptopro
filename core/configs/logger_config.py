from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class LoggerConfig:
    """Конфигурация логгера — неизменяемые данные для передачи настроек. Используется как DTO."""

    name: str | None = None
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    format: str = (
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    use_colors: bool = False
