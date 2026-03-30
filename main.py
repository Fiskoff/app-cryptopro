import asyncio

from app.core import settings, GirVuAuthError, CertificateNotFoundError
from app.core.configs.logger_config import LoggerConfig
from app.core.loger_manager import LoggerManager
from app.services import CryptoProService
from app.clients import GetTokenUseCase


config = LoggerConfig(name="main", level="DEBUG")
logger = LoggerManager.setup(config)

async def main():
    logger.info("Запуск процедуры авторизации ГИР ВУ")
    try:
        thumbprint = settings.auth.certificate_thumbprint
        crypto_service = CryptoProService(thumbprint=thumbprint)
        use_case_get_token = GetTokenUseCase(settings=settings, crypto_service=crypto_service)
        auth_result = await use_case_get_token.execute()
        logger.info(f"Token: {auth_result['token'][:10]}")


    except CertificateNotFoundError as error:
        logger.error(f"Ошибка сертификата: {error}")
    except GirVuAuthError as error:
        logger.error(f"Ошибка авторизации: {error}")
    except Exception as error:
        logger.exception(f"Критическая ошибка: {error}")


if __name__ == "__main__":
    asyncio.run(main())