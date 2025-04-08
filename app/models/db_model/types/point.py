from typing import Any, List, Optional

from sqlalchemy import BINARY, DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType
import datetime
from sqlalchemy.types import UserDefinedType
from app.models.db_model.base import Base
from sqlalchemy.sql import func

class Point(UserDefinedType):
    def get_col_spec(self):
        return "POINT"

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            return f"POINT({value.x} {value.y})"
        return process

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, 4326)

    def column_expression(self, col):
        return func.AsText(col)