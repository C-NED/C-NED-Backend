from __future__ import annotations

from typing import Any, List, Optional

from sqlalchemy import DateTime, Index, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
from app.auth.relationships import roadinfo_caution_join,roadinfo_outbreak_join,roadinfo_vsl_join
# from app.models.db_model.caution import Caution
# from app.models.db_model.outbreak import Outbreak
# from app.models.db_model.vsl import Vsl


class RoadInfo(Base):
    __tablename__ = 'road_info'
    __table_args__ = (
        Index('road_no', 'road_no'),
        UniqueConstraint("route_no", "route_name", name="uix_route_road"),
    )

    route_no: Mapped[str] = mapped_column(String(10), primary_key=True)
    road_no: Mapped[str] = mapped_column(String(10))
    route_name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    # road_info_caution_to: Mapped[List['Caution']] = relationship('Caution', back_populates='road_info_caution_from')
    # road_info_outbreak_to: Mapped[List['Outbreak']] = relationship('Outbreak', back_populates='road_info_outbreak_from')
    # road_info_vsl_to: Mapped[List['Vsl']] = relationship('Vsl', back_populates='road_info_vsl_from')

    #다형성 FK 정의
    roadinfo_caution_to: Mapped[Optional['Caution']] = relationship(
        'Caution',
        primaryjoin=roadinfo_caution_join,
        back_populates='roadinfo_caution_from',
        viewonly=True,
        lazy='raise'
    )

    roadinfo_outbreak_to: Mapped[Optional['Outbreak']] = relationship(
        'Outbreak',
        primaryjoin=roadinfo_outbreak_join,
        back_populates='roadinfo_outbreak_from',
        viewonly=True,
        lazy='raise'
    )

    roadinfo_vsl_to: Mapped[Optional['Vsl']] = relationship(
        'Vsl',
        primaryjoin=roadinfo_vsl_join,
        back_populates='roadinfo_vsl_from',
        viewonly=True,
        lazy='raise'
    )