import logging

import httpx

from app.core import Settings, GirVuAuthError, SigningError, CertificateNotFoundError
from app.services import CryptoProService


logger = logging.getLogger(__name__)


class GirVuAuthClient:
    """Клиент для авторизации в системе ГИР ВУ. Реализует процедуру получения токена"""
    def __init__(self, settings: Settings, crypto_service: CryptoProService):
        self.settings = settings
        self.crypto = crypto_service
        self._token: str | None = None

        self.http_client = httpx.Client(timeout=30.0)

    def _prepare_payload(self) -> dict:
        """
        Формирует payload для запроса авторизации

        Returns:
            dict: Словарь для отправки в POST-запросе

        Raises:
            GirVuAuthError: Если ошибка при подписании
        """
        try:
            data_to_sign = self.settings.signature_string
            signature_b64 = self.crypto.signature_data(data_to_sign)
            logger.debug("Данные успешно подписаны")

            payload = {
                "organization": {
                    "ogrn": self.settings.OGRN,
                    "kpp": self.settings.KPP
                },
                "sign": signature_b64
            }
            return payload

        except (SigningError, CertificateNotFoundError) as error:
            logger.error(f"Не удалось подготовить данные для авторизации: {error}")
            raise GirVuAuthError(f"Ошибка подготовки подписи: {error}") from error

    def login(self) -> str:
        """
        Выполняет запрос на получение токена.

        Returns:
            str: Полученный токен доступа.

        Raises:
            GirVuAuthError: Если сервер вернул ошибку или токен отсутствует.
        """
        if self._token:
            logger.warning("Токен уже получен")

        try:
            payload = self._prepare_payload()
            headers = {"Content-Type": "application/json"}

            logger.info(f"Отправка запроса авторизации на {self.settings.api_url}")

            response = self.http_client.post(
                url=self.settings.api_url,
                json=payload,
                headers=headers
            )

            if response.status_code == 200:
                response_data = response.json()
                token = response_data.get("token")

                if not token:
                    raise GirVuAuthError("Сервер вернул статус 200, но поле 'token' отсутствует в ответе.")

                self._token = token
                logger.info("Токен получен")
                return token

            else:
                error_detail = response.text
                logger.error(f"Ошибка авторизации. Статус: {response.status_code}. Ответ: {error_detail}")
                raise GirVuAuthError(
                    f"HTTP {response.status_code}: Не удалось получить токен. "
                    f"Детали: {error_detail}"
                )

        except httpx.RequestError as error:
            logger.exception("Сетевая ошибка при подключении к ГИР ВУ")
            raise GirVuAuthError(f"Не удалось соединиться с сервером: {error}") from error
        except Exception as error:
            if isinstance(error, GirVuAuthError):
                raise
            logger.exception("Непредвиденная ошибка при авторизации")
            raise GirVuAuthError(f"Внутренняя ошибка клиента: {error}") from error

    @property
    def token(self) -> str | None:
        """Возвращает текущий активный токен."""
        return self._token

    def get_auth_headers(self) -> dict:
        """
        Возвращает заголовки для последующих запросов к API.

        Returns:
            dict: Словарь заголовков.

        Raises:
            GirVuAuthError: Если токен еще не получен.
        """
        if not self._token:
            raise GirVuAuthError("Токен не получен. Сначала вызовите метод login().")

        return {
            "Student-Authorization": self._token,
            "Content-Type": "application/json"
        }

    def close(self):
        """Закрытие HTTP сессии."""
        self.http_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()