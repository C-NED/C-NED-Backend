from typing import Any, List, Optional

from sqlalchemy import BINARY, DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType
import datetime
from sqlalchemy.types import UserDefinedType
from app.models.db_model.base import Base

class Admin(Base):
    __tablename__ = 'admin'
    __table_args__ = (
        Index('idx_principal', 'admin_id', 'admin_type'),
    )

    admin_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    admin_type: Mapped[str] = mapped_column(Enum('ROAD', 'SERVICE'))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(50))
    profile_img: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))
