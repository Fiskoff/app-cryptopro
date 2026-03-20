import logging
from typing import Any

import pycades

from core.cryptopro_config import CryptoConstants
from exceptions import CertificateNotFoundError


logger = logging.getLogger(__name__)


class CryptoProService:
    """
    Сервис для работы с криптопровайдером CryptoPro CSP через pycades.
    Предназначен для подписи данных в формате, требуемом API ГИР ВУ.
    """

    def __init__(self, thumbprint: str):
        self._thumbprint = thumbprint
        self._certificate_cache: Any | None = None

    def _get_certificate(self) -> Any:
        """
        Получает объект сертификата из кэша или ищет его в хранилище. Реализует паттерн Lazy Loading
        Находит и возвращает объект сертификата из личного хранилища текущего пользователя по отпечатку

        Returns:
            pycades.Certificate: Объект сертификата.

        Raises:
            CertificateNotFoundError: Если сертификат не найден или у него нет закрытого ключа
        """

        if self._certificate_cache is not None:
            return self._certificate_cache

        store: pycades.Store | None = None
        try:
            logger.debug(f"Поиск сертификата с отпечатком: {self._thumbprint}")
            store = pycades.Store()
            store.Open(
                CryptoConstants.STORE_LOCATION,
                CryptoConstants.STORE_NAME,
                CryptoConstants.STORE_FLAGS
            )

            certificates_collection = store.Certificates.FindByThumbprint(self._thumbprint)

            if certificates_collection.Count == 0:
                raise CertificateNotFoundError(
                    f"Сертификат '{self._thumbprint}' не найден в хранилищеCurrentUser\\MY. "
                    f"Проверьте установку сертификата и доступность токена."
                )

            certificate = certificates_collection.Item(1)
            self._validate_certificate_object(certificate, self._thumbprint)
            self._certificate_cache = certificate
            logger.info(f"Сертификат успешно загружен: {certificate.SubjectName}")
            return certificate

        except Exception as error:
            logger.error(f"Ошибка доступа к хранилищу сертификатов: {error}")
            if isinstance(error, CertificateNotFoundError):
                raise
            raise CertificateNotFoundError(f"Не удалось получить сертификат: {error}") from error

        finally:
            if store is not None:
                try:
                    store.Close()
                except Exception as error:
                    logger.warning(f"{error}: Не удалось закрыть хранилище сертификатов")

    @staticmethod
    def _validate_certificate_object(certificate: Any, thumbprint: str) -> None:
        """
        Проверяет объект сертификата на наличие закрытого ключа

        Args:
            certificate (Any): Объект pycades.Certificate
            thumbprint (str): Отпечаток сертификата

        Raises:
            CertificateNotFoundError: Если у сертификата нет закрытого ключа.
        """

        if not certificate.HasPrivateKey:
            logger.error(f"У сертификата '{thumbprint}' отсутствует закрытый ключ.")
            raise CertificateNotFoundError(
                f"Сертификат '{thumbprint}' найден, но у него отсутствует закрытый ключ. "
                f"Подпись невозможна. Убедитесь, что контейнер закрытого ключа установлен и доступен."
            )
        logger.debug(f"Проверка закрытого ключа для '{thumbprint}' успешна.")