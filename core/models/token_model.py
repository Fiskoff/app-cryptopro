from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base_model import BaseModel


class TokenModel(BaseModel):
    """ORM модель таблицы auth_tokens"""

    __tablename__ = 'auth_tokens'
    __table_args__ = (
        Index("ix_gir_token_active", "is_active", "expires_at"),
        Index("ix_gir_token_created", "created_at"),
        {"schema": "gir"},
    )

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    token: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,default=True, nullable=False, index=True
    )
    is_revoked: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )