from __future__ import annotations

from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
from app.models.db_model.types.point import Point
# from app.models.db_model.navigation import Navigation
from app.models.db_model.road_info import RoadInfo
# from app.models.db_model.admin import Admin
# from app.models.db_model.user import User
from app.auth.relationships import admin_outbreak_join,user_outbreak_join

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

    navigation_outbreak_from: Mapped['Navigation'] = relationship('Navigation', back_populates='navigation_outbreak_to')
    road_info_outbreak_from: Mapped['RoadInfo'] = relationship('RoadInfo', back_populates='road_info_outbreak_to')

     #다형성 fk 정의 
    user_outbreak_from: Mapped[Optional['User']] = relationship(
        'User',
        primaryjoin=user_outbreak_join,
        back_populates='user_outbreak_to',
        viewonly=True,
        lazy='raise',
        overlaps="admin_outbreak_from"
    )

    admin_outbreak_from: Mapped[Optional['Admin']] = relationship(
        'Admin',
        primaryjoin=admin_outbreak_join,
        back_populates='admin_outbreak_to',
        viewonly=True,
        lazy='raise'
    )
