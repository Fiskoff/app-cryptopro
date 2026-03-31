from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """Базовая модель всех ORM моделей. Содержит метаданные всех моделей, которые от неё наследованные"""
    pass