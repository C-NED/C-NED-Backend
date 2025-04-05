from __future__ import annotations

from typing import Any, List, Optional

from sqlalchemy import DateTime, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
# from app.models.db_model.caution import Caution
# from app.models.db_model.outbreak import Outbreak
# from app.models.db_model.vsl import Vsl


class RoadInfo(Base):
    __tablename__ = 'road_info'
    __table_args__ = (
        Index('road_no', 'road_no', unique=True),
    )

    route_no: Mapped[str] = mapped_column(String(10), primary_key=True)
    road_no: Mapped[str] = mapped_column(String(10))
    route_name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    caution: Mapped[List['Caution']] = relationship('Caution', back_populates='road_info')
    outbreak: Mapped[List['Outbreak']] = relationship('Outbreak', back_populates='road_info')
    vsl: Mapped[List['Vsl']] = relationship('Vsl', back_populates='road_info')