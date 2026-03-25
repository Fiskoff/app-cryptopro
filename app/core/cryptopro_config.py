import pycades


class CryptoConstants:
    """
    Константы конфигурации для работы с CryptoPro CSP в рамках интеграции с ГИР ВУ.
    https://docs.cryptopro.ru/cades/plugin/plugin-methods?id=%d0%9a%d0%be%d0%bd%d1%81%d1%82%d0%b0%d0%bd%d1%82%d1%8b
    """

    STORE_LOCATION = pycades.CAPICOM_CURRENT_USER_STORE
    STORE_NAME = pycades.CAPICOM_MY_STORE
    STORE_FLAGS = pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED

    HASH_ALGO = pycades.CADESCOM_HASH_ALGORITHM_CP_GOST_3411_2012_256

    SIGNATURE_OPTION = 1
    CONTENT_TYPE = 0