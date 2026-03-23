class CertificateNotFoundError(Exception):
    """Исключение, когда сертификат не найден в хранилище."""
    pass

class SigningError(Exception):
    """Исключение ошибки при создании подписи."""
    pass
