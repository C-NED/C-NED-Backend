from __future__ import annotations
from typing import Any, List, Optional

from sqlalchemy import DateTime, Enum, Index, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
from app.models.db_model.types.point import Point
# from app.models.db_model.caution import Caution
# from app.models.db_model.dangerous_incident import DangerousIncident
# from app.models.db_model.vsl import Vsl
# from app.models.db_model.outbreak import Outbreak
# from app.models.db_model.path import Path
# from app.models.db_model.user import User
# from app.models.db_model.admin import Admin
# from app.models.db_model.road_section import RoadSection
from app.auth.relationships import user_navigation_join,admin_navigation_join


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

    navigation_caution_to : Mapped[List['Caution']] = relationship('Caution', back_populates='navigation_caution_from')
    navigation_dangerous_to: Mapped[List['DangerousIncident']] = relationship('DangerousIncident', back_populates='navigation_dangerous_from')
    navigation_outbreak_to: Mapped[List['Outbreak']] = relationship('Outbreak', back_populates='navigation_outbreak_from')
    navigation_path_to: Mapped[List['Path']] = relationship('Path', back_populates='navigation_path_from')
    navigation_vsl_to: Mapped[List['Vsl']] = relationship('Vsl', back_populates='navigation_vsl_from')
    navigation_road_section_to: Mapped[List['RoadSection']] = relationship('RoadSection', back_populates='navigation_road_section_from')

    #다형성 fk 정의
    # Navigation 입장에서 관계 정의 (반대 방향)
    user_navigation_from: Mapped[Optional['User']] = relationship(
        'User',
        primaryjoin=user_navigation_join,
        back_populates='user_navigation_to',
        viewonly=True,
        lazy='raise',
        overlaps="admin_navigation_from"
    )

    admin_navigation_from: Mapped[Optional['Admin']] = relationship(
        'Admin',
        primaryjoin=admin_navigation_join,
        back_populates='admin_navigation_to',
        viewonly=True,
        lazy='raise'
    )
