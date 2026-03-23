import logging

from app.core import setup_logger, settings, GirVuAuthError, CertificateNotFoundError
from app.services import CryptoProService
from app.clients import GetTokenUseCase


setup_logger(level="DEBUG")
logger = logging.getLogger(__name__)

def main():
    logger.info("Запуск процедуры авторизации ГИР ВУ")
    try:
        thumbprint = settings.auth.certificate_thumbprint
        crypto_service = CryptoProService(thumbprint=thumbprint)

        use_case_get_token = GetTokenUseCase(settings=settings.auth, crypto_service=crypto_service)
        result = use_case_get_token.execute()

        logger.info(f"Token: {result['token']}")

    except CertificateNotFoundError as error:
        logger.error(f"Ошибка сертификата: {error}")

    except GirVuAuthError as error:
        logger.error(f"Ошибка авторизации: {error}")

    except Exception as error:
        logger.exception(f"Критическая ошибка: {error}")


if __name__ == "__main__":
    main()