from __future__ import annotations

from typing import Any, List, Optional

from sqlalchemy import BINARY, DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
# from app.models.db_model.navigation import Navigation
# from app.models.db_model.path import Path

class RoadSection(Base):
    __tablename__ = 'road_section'
    __table_args__ = (
        ForeignKeyConstraint(['navigation_id'], ['navigation.navigation_id'], ondelete='CASCADE', onupdate='CASCADE', name='road_section_ibfk_1'),
        # ForeignKeyConstraint(['path_id'], ['path.path_id'], ondelete='CASCADE', onupdate='CASCADE', name='road_section_ibfk_2'),
        Index('navigation_id', 'navigation_id'),
        # Index('path_id', 'path_id')
    )

    road_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11))
    name: Mapped[str] = mapped_column(String(30))
    distance: Mapped[int] = mapped_column(INTEGER(11))
    speed: Mapped[int] = mapped_column(INTEGER(11))
    congestion: Mapped[str] = mapped_column(Enum('정보 없음', '원활', '서행', '혼잡'))
    pointidx : Mapped[int] = mapped_column(INTEGER(11))
    pointcount : Mapped[int] = mapped_column(INTEGER(11))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation_road_section_from: Mapped['Navigation'] = relationship('Navigation', back_populates='navigation_road_section_to')
