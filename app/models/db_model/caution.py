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
from app.auth.relationships import admin_caution_join,user_caution_join


class Caution(Base):
    __tablename__ = 'caution'
    __table_args__ = (
        ForeignKeyConstraint(['navigation_id'], ['navigation.navigation_id'], ondelete='CASCADE', onupdate='CASCADE', name='caution_ibfk_1'),
        ForeignKeyConstraint(['route_no'], ['road_info.route_no'], ondelete='CASCADE', onupdate='CASCADE', name='caution_ibfk_2'),
        Index('navigation_id', 'navigation_id'),
        Index('route_no', 'route_no')
    )

    caution_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_type: Mapped[str] = mapped_column(Enum('USER','ROAD_ADMIN', 'SERVICE_ADMIN'))
    message: Mapped[str] = mapped_column(String(100))
    loc: Mapped[Point] = mapped_column(Point)
    route_no: Mapped[str] = mapped_column(String(10))
    route_name: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation: Mapped['Navigation'] = relationship('Navigation', back_populates='caution')
    road_info: Mapped['RoadInfo'] = relationship('RoadInfo', back_populates='caution')

    #다형성 fk 정의 
    user_caution_from: Mapped[Optional['User']] = relationship(
        'User',
        primaryjoin=user_caution_join,
        back_populates='user_caution_to',
        viewonly=True,
        lazy='raise'
    )

    admin_caution_from: Mapped[Optional['Admin']] = relationship(
        'Admin',
        primaryjoin=admin_caution_join,
        back_populates='admin_caution_to',
        viewonly=True,
        lazy='raise'
    )