import logging
import base64
from typing import Any

import pycades

from app.core import CryptoConstants
from app.core import SigningError, CertificateNotFoundError


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

    def signature_data(self, data: str) -> str:
        """
        Создает открепленную электронную подпись (Detached Signature) для строки данных
        Использует ГОСТ Р 34.11-2012 (256 бит), результат кодируется в Base64

        Args:
            data (str): Строка данных для подписи (строка 'ОГРН+КПП').

        Returns:
            str: Подпись в формате Base64.

        Raises:
            SigningError: Если процесс подписания не удался.
        """

        if not data:
            raise ValueError("Данные для подписи не могут быть пустыми.")

        try:
            certificate = self._get_certificate()

            content_info = pycades.ContentInfo()
            content_info.ContentType = CryptoConstants.CONTENT_TYPE
            content_info.Content = data.encode('utf-8')

            cp_signature = pycades.CPSignature()
            cp_signature.SignerCertificate = certificate
            cp_signature.Options = CryptoConstants.SIGNATURE_OPTION
            cp_signature.HashAlgorithm.Algorithm = CryptoConstants.HASH_ALGO

            signature_bytes = cp_signature.SignContent(content_info)
            signature_b64 = base64.b64encode(signature_bytes).decode('ascii')

            logger.debug(f"Успешно создана подпись длиной {len(signature_b64)} символов.")
            return signature_b64

        except Exception as error:
            logger.exception("Критическая ошибка при создании подписи")
            raise SigningError(f"Не удалось подписать данные: {error}") from error

    @property
    def subject_name(self) -> str:
        """Возвращает имя владельца сертификата (Subject Name)."""
        return self._get_certificate().SubjectName

    @property
    def thumbprint(self) -> str:
        """Возвращает отпечаток сертификата."""
        return self._thumbprint
