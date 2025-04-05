from typing import Any, List, Optional

from sqlalchemy import BINARY, DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType
import datetime
from sqlalchemy.types import UserDefinedType
from app.models.db_model.base import Base
from app.models.db_model.point import Point
from app.models.db_model.navigation import Navigation
from app.models.db_model.road_info import RoadInfo

class Outbreak(Base):
    __tablename__ = 'outbreak'
    __table_args__ = (
        ForeignKeyConstraint(['navigation_id'], ['navigation.navigation_id'], ondelete='CASCADE', onupdate='CASCADE', name='outbreak_ibfk_1'),
        ForeignKeyConstraint(['road_no'], ['road_info.road_no'], ondelete='CASCADE', onupdate='CASCADE', name='outbreak_ibfk_2'),
        Index('navigation_id', 'navigation_id'),
        Index('road_no', 'road_no')
    )

    outbreak_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_type: Mapped[str] = mapped_column(Enum('USER','ROAD_ADMIN', 'SERVICE_ADMIN'))
    event_type: Mapped[str] = mapped_column(String(10))
    period: Mapped[str] = mapped_column(String(15))
    road_name: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(String(100))
    loc: Mapped[Point] = mapped_column(Point)
    road_no: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation: Mapped['Navigation'] = relationship('Navigation', back_populates='outbreak')
    road_info: Mapped['RoadInfo'] = relationship('RoadInfo', back_populates='outbreak')
