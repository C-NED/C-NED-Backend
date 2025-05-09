from __future__ import annotations

from typing import Any, List, Optional

from sqlalchemy import BINARY, DateTime, Enum, Index, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import Mapped, mapped_column,relationship
import datetime
from app.models.db_model.base import Base
from app.auth.relationships import user_refresh_join,admin_refresh_join

class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    __table_args__ = (
        Index('idx_principal', 'principal_type', 'principal_id'),
        Index('refresh_token', 'refresh_token', unique=True)
    )

    refresh_token_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    principal_type: Mapped[str] = mapped_column(Enum('USER', 'ADMIN'))
    principal_id: Mapped[int] = mapped_column(INTEGER(11))
    refresh_token: Mapped[bytes] = mapped_column(BINARY(32))
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    revoked: Mapped[Optional[int]] = mapped_column(TINYINT(4), server_default=text('0'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    #다형성 fk 처리

    user_refresh_from : Mapped[List['User']] = relationship(
        'User',
        primaryjoin=user_refresh_join,
        back_populates='user_refresh_to',
        lazy='raise',
        viewonly=True,
        overlaps="admin_refresh_from"
    )

    admin_refresh_from: Mapped[List['Admin']] = relationship(
        'Admin',
        primaryjoin=admin_refresh_join,
        back_populates='admin_refresh_to',
        lazy='raise',
        viewonly=True,
    )