from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
from app.models.db_model.types.point import Point
# from app.models.db_model.admin import Admin
# from app.models.db_model.user import User
# from app.models.db_model.navigation import Navigation
# from app.models.db_model.road_info import RoadInfo
from app.auth.relationships import user_vsl_join,admin_vsl_join,roadinfo_vsl_join



class Vsl(Base):
    __tablename__ = 'vsl'
    __table_args__ = (
        ForeignKeyConstraint(['navigation_id'], ['navigation.navigation_id'], ondelete='CASCADE', onupdate='CASCADE', name='vsl_ibfk_1'),
        ForeignKeyConstraint(['road_no'], ['road_info.road_no'], ondelete='CASCADE', onupdate='CASCADE', name='vsl_ibfk_2'),
        Index('navigation_id', 'navigation_id'),
        Index('road_no', 'road_no')
    )

    vsl_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_type: Mapped[str] = mapped_column(Enum('USER','ROAD_ADMIN', 'SERVICE_ADMIN'))
    vsl_name: Mapped[str] = mapped_column(String(50))
    loc: Mapped[Point] = mapped_column(Point)
    registedDate: Mapped[str] = mapped_column(String(50))
    road_no: Mapped[str] = mapped_column(String(10))
    default_speed_limit: Mapped[int] = mapped_column(INTEGER(11))
    cur_speed_limit: Mapped[int] = mapped_column(INTEGER(11))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation_vsl_from: Mapped['Navigation'] = relationship('Navigation', back_populates='navigation_vsl_to')
    # road_info_vsl_from: Mapped['RoadInfo'] = relationship('RoadInfo', back_populates='road_info_vsl_to')


     #다형성 fk 정의 
    user_vsl_from: Mapped[Optional['User']] = relationship(
        'User',
        primaryjoin=user_vsl_join,
        viewonly=True,
        back_populates='user_vsl_to',
        lazy='raise',
        overlaps="admin_vsl_from"
    )

    admin_vsl_from: Mapped[Optional['Admin']] = relationship(
        'Admin',
        primaryjoin=admin_vsl_join,
        viewonly=True,
        back_populates='admin_vsl_to',
        lazy='raise'
    )

    roadinfo_vsl_from: Mapped[Optional['RoadInfo']] = relationship(
        'RoadInfo',
        primaryjoin=roadinfo_vsl_join,
        back_populates='roadinfo_vsl_to',
        viewonly=True,
        lazy='raise'
    )