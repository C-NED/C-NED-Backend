from typing import Any, List, Optional

from sqlalchemy import BINARY, DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType
import datetime
from sqlalchemy.types import UserDefinedType
from app.models.db_model.base import Base

class Point(UserDefinedType):
    def get_col_spec(self, **kw):
        return "POINT"

    def bind_expression(self, bindvalue):
        return bindvalue

    def column_expression(self, col):
        return col