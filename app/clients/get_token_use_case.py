import logging
from typing import Dict, Any

from app.core import Settings, GirVuAuthError
from app.services import CryptoProService
from app.clients import GirVuAuthClient


logger = logging.getLogger(__name__)


class GetTokenUseCase:
    """Сценарий использования для получения токена авторизации ГИР ВУ."""

    def __init__(self, settings: Settings, crypto_service: CryptoProService):
        self.settings = settings
        self.crypto = crypto_service

    def execute(self) -> Dict[str, Any]:
        """
        Выполняет полный цикл авторизации.

        Returns:
            dict: Словарь с результатом:
                {
                    "token": (str) Сам токен
                    "headers": (dict) Заголовки для последующих запросов
                    "subject_name": (str) Имя владельца сертификата
                }

        Raises:
            CertificateNotFoundError: Если сертификат не найден или невалиден.
            GirVuAuthError: Если ошибка при запросе к серверу ГИР ВУ.
            Exception: Любая другая непредвиденная ошибка.
        """
        thumbprint = self.settings.auth.certificate_thumbprint
        logger.info(f"Инициализация сценария получения токена для отпечатка: {thumbprint}")

        try:
            with GirVuAuthClient(settings=self.settings, crypto_service=self.crypto) as client:
                auth_token = client.login()
                logger.info("Токен успешно получен от сервера ГИР ВУ")

                headers = client.get_auth_headers()

                logger.debug(f"Сформированы заголовки: Student-Authorization: {auth_token[:10]}...")

                return {
                    "token": auth_token,
                    "headers": headers,
                }

        except GirVuAuthError:
            raise
        except Exception as e:
            logger.exception("Произошла непредвиденная ошибка в процессе авторизации")
            raise GirVuAuthError(f"Внутренняя ошибка сценария авторизации: {e}") from e