import logging
from typing import Any

import pycades

from app.core import CryptoConstants, SigningError, CertificateNotFoundError


logger = logging.getLogger(__name__)


class CryptoProService:
    """Сервис для работы с криптопровайдером CryptoPro CSP через pycades."""

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
            logger.debug(f"Поиск сертификата с отпечатком: {self._thumbprint[:20]}...")
            store = pycades.Store()
            store.Open(
                CryptoConstants.STORE_LOCATION,
                CryptoConstants.STORE_NAME,
                CryptoConstants.STORE_FLAGS
            )

            certificates = store.Certificates
            count = certificates.Count

            for i in range(1, count + 1):
                certificate = certificates.Item(i)
                if certificate.Thumbprint.lower() == self._thumbprint.lower():
                    if not certificate.HasPrivateKey():
                        raise CertificateNotFoundError(
                            f"Сертификат '{self._thumbprint[:20]}...' найден, но закрытый ключ недоступен. "
                            f"Проверьте доступность токена."
                        )
                    self._certificate_cache = certificate
                    logger.info(f"Сертификат успешно загружен: {certificate.SubjectName}")
                    return certificate

            raise CertificateNotFoundError(
                f"Сертификат '{self._thumbprint[:20]}...' не найден в хранилище CurrentUser\\MY. "
            )

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
            logger.error(f"У сертификата '{thumbprint[:20]}...' отсутствует закрытый ключ.")
            raise CertificateNotFoundError(
                f"Сертификат '{thumbprint[:20]}...' найден, но у него отсутствует закрытый ключ. "
                f"Подпись невозможна. Убедитесь, что контейнер закрытого ключа установлен и доступен."
            )
        logger.debug(f"Проверка закрытого ключа для '{thumbprint[:20]}...' успешна.")

    async def signature_data(self, data_str: str) -> str:
        """
        Создание откреплённой электронной подписи (CAdES-BES)

        Args:
            data_str (str): Строка данных для подписи (строка 'ОГРН+КПП').

        Returns:
            str: Подпись в формате Base64.

        Raises:
            SigningError: Если процесс подписания не удался.

        """

        try:
            logger.debug(f"Подпись данных (длина: {len(data_str)})")

            certificate = self._get_certificate()

            signer = pycades.Signer()
            signer.Certificate = certificate
            signer.CheckCertificate = True
            signer.Options = CryptoConstants.SIGNATURE_OPTION

            signed_data = pycades.SignedData()
            signed_data.Content = data_str

            signature_base64 = signed_data.SignCades(signer, pycades.CADESCOM_CADES_BES)

            logger.info("Подпись успешно создана")
            return signature_base64

        except CertificateNotFoundError:
            raise
        except AttributeError as error:
            logger.error(f"Ошибка API pycades: {error}")
            raise SigningError(f"Неверный вызов pycades API: {error}")
        except Exception as error:
            logger.error(f"Критическая ошибка при создании подписи", exc_info=True)
            raise SigningError(f"Не удалось подписать данные: {error}")

    @property
    def subject_name(self) -> str:
        """Возвращает имя владельца сертификата (Subject Name)."""
        return self._get_certificate().SubjectName

    @property
    def thumbprint(self) -> str:
        """Возвращает отпечаток сертификата."""
        return self._thumbprint
