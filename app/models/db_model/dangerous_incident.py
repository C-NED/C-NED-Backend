from __future__ import annotations

from typing import Any, List, Optional

from sqlalchemy import DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
from app.models.db_model.types.point import Point
# from app.models.db_model.navigation import Navigation
# from app.models.db_model.admin import Admin
# from app.models.db_model.user import User
from app.auth.relationships import admin_dangerous_join,user_dangerous_join

class DangerousIncident(Base):
    __tablename__ = 'dangerous_incident'
    __table_args__ = (
        ForeignKeyConstraint(['navigation_id'], ['navigation.navigation_id'], ondelete='CASCADE', onupdate='CASCADE', name='dangerous_incident_ibfk_1'),
        Index('navigation_id', 'navigation_id')
    )

    dincident_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_type: Mapped[str] = mapped_column(Enum('USER','ROAD_ADMIN', 'SERVICE_ADMIN'))
    loc: Mapped[Point] = mapped_column(Point)
    period: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation_dangerous_from: Mapped['Navigation'] = relationship('Navigation', back_populates='navigation_dangerous_to')

    #다형성 fk 정의 
    user_dangerous_incident_from: Mapped[Optional['User']] = relationship(
        'User',
        primaryjoin=user_dangerous_join,
        back_populates='user_dangerous_incident_to',
        viewonly=True,
        lazy='raise',
        overlaps="admin_dangerous_incident_from"
    )

    admin_dangerous_incident_from: Mapped[Optional['Admin']] = relationship(
        'Admin',
        primaryjoin=admin_dangerous_join,
        back_populates='admin_dangerous_incident_to',
        viewonly=True,
        lazy='raise'
    )
