from typing import Any, List, Optional

from sqlalchemy import BINARY, DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType
import datetime
from sqlalchemy.types import UserDefinedType
from app.models.db_model.base import Base
from app.models.db_model.point import Point
from app.models.db_model.caution import Caution
from app.models.db_model.dangerous_incident import DangerousIncident
from app.models.db_model.vsl import Vsl
from app.models.db_model.outbreak import Outbreak
from app.models.db_model.path import Path
from app.models.db_model.road_section import RoadSection


class Navigation(Base):
    __tablename__ = 'navigation'
    __table_args__ = (
        Index('end_loc', 'end_loc'),
        Index('start_loc', 'start_loc'),
    )

    navigation_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    principal_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_type: Mapped[str] = mapped_column(Enum('USER','ROAD_ADMIN', 'SERVICE_ADMIN'))
    start_loc: Mapped[Point] = mapped_column(Point)
    end_loc: Mapped[Point] = mapped_column(Point)
    arrival_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    road_option: Mapped[str] = mapped_column(Enum('trafast', 'tracomfort', 'traoptimal', 'traviodtoll', 'traavoidcaronly'))
    total_distance: Mapped[int] = mapped_column(INTEGER(11))
    total_time: Mapped[int] = mapped_column(INTEGER(11))
    taxifare: Mapped[int] = mapped_column(INTEGER(11))
    tollfare: Mapped[int] = mapped_column(INTEGER(11))
    fuelprice: Mapped[int] = mapped_column(INTEGER(11))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    caution: Mapped[List['Caution']] = relationship('Caution', back_populates='navigation')
    dangerous_incident: Mapped[List['DangerousIncident']] = relationship('DangerousIncident', back_populates='navigation')
    outbreak: Mapped[List['Outbreak']] = relationship('Outbreak', back_populates='navigation')
    path: Mapped[List['Path']] = relationship('Path', back_populates='navigation')
    vsl: Mapped[List['Vsl']] = relationship('Vsl', back_populates='navigation')
    road_section: Mapped[List['RoadSection']] = relationship('RoadSection', back_populates='navigation')
