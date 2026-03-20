import pycades


class CryptoConstants:
    """
    Константы конфигурации для работы с CryptoPro CSP в рамках интеграции с ГИР ВУ.
    Все значения соответствуют требованиям инструкции API (версия 1.1.4).

    Работа с хранилищем:
        CAPICOM_CURRENT_USER_STORE: Хранилище текущего пользователя
        CAPICOM_MY_STORE: Имя хранилища «Личные», содержит сертификаты с закрытыми ключами, необходимыми для подписи
        CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED: Флаг доступа «Максимально разрешенный». Позволяет читать сертификат и использовать закрытый ключ для операций

    Алгоритмы шифрования:
        CAPICOM_HASH_ALGORITHM_GOST_3411_2012_256: Алгоритм шифрования, стандарт для УКЭП в гос системах (ГИР ВУ) - ГОСТ Р 34.11-2012 (256 бит)

    Параметры подписи:
        CAPICOM_SIGNATURE_OPTION_DETACHED: Открепленная подпись. Подпись формируется отдельно от данных. Требуется инструкцией ГИР ВУ (п. 3.1, 3.4.1), так как данные передаются в поле "data", а подпись в поле "sign"
        CAPICOM_CONTENT_DATA: Указывает, что подписываемый объект является потоком байтов (строкой JSON или ОГРН+КПП), а не вложенной структурой CMS
    """

    STORE_LOCATION = pycades.CAPICOM_CURRENT_USER_STORE
    STORE_NAME = pycades.CAPICOM_MY_STORE
    STORE_FLAGS = pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED

    HASH_ALGO = pycades.CAPICOM_HASH_ALGORITHM_GOST_3411_2012_256

    SIGNATURE_OPTION = pycades.CAPICOM_SIGNATURE_OPTION_DETACHED
    CONTENT_TYPE = pycades.CAPICOM_CONTENT_DATA