class CertificateNotFoundError(Exception):
    """Исключение, когда сертификат не найден в хранилище."""
    pass


class SigningError(Exception):
    """Исключение ошибки при создании подписи."""
    pass


class GirVuError(Exception):
    """Базовое исключение для ошибок интеграции с ГИР ВУ."""
    pass


class GirVuAuthError(GirVuError):
    """Ошибка авторизации (получения токена)."""
    pass


class TokenError(Exception):
    """Базовое исключение для токенов."""

    pass


class TokenNotFoundError(TokenError):
    """Токен не найден."""

    pass


class TokenExpiredError(TokenError):
    """Токен истёк."""

    pass


class TokenInvalidError(TokenError):
    """Токен невалиден."""

    pass


class EncryptionError(TokenError):
    """Ошибка шифрования/дешифрования."""

    pass

