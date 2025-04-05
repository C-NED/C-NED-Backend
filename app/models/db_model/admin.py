from __future__ import annotations

from typing import Any, List, Optional

from sqlalchemy import DateTime, Enum,Index, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
from app.auth.relationships import admin_navigation_join,admin_caution_join,admin_dangerous_join,admin_outbreak_join,admin_vsl_join
# from app.models.db_model.navigation import Navigation
# from app.models.db_model.outbreak import Outbreak
# from app.models.db_model.vsl import Vsl
# from app.models.db_model.caution import Caution
# from app.models.db_model.dangerous_incident import DangerousIncident


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

    #다형성 fk 정의

    admin_navigation_to: Mapped[List['Navigation']] = relationship(
    'Navigation',
    primaryjoin=admin_navigation_join,
    back_populates='admin_navigation_from',
    lazy='raise'
    )

    admin_outbreak_to: Mapped[List['Outbreak']] = relationship(
    'Outbreak',
    primaryjoin=admin_outbreak_join,
    back_populates='admin_outbreak_from',
    lazy='raise'
    )

    admin_vsl_to: Mapped[List['Vsl']] = relationship(
    'Vsl',
    primaryjoin=admin_vsl_join,
    back_populates='admin_vsl_from',
    lazy='raise'
    )

    admin_caution_to: Mapped[List['Caution']] = relationship(
    'Caution',
    primaryjoin=admin_caution_join,
    back_populates='admin_caution_from',
    lazy='raise'
    )

    #dangerous_incident의 경우 list지만, 네이밍 일관성(편의)를 위해 단수형으로 표기함
    admin_dangerous_incident_to: Mapped[List['DangerousIncident']] = relationship(
    'DangerousIncident',
    primaryjoin=admin_dangerous_join,
    back_populates='admin_dangerous_incident_from',
    lazy='raise'
    )