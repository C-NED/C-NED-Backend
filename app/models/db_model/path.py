from __future__ import annotations

from typing import List, Optional

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
from app.models.db_model.types.point import Point
# from app.models.db_model.navigation import Navigation
from app.models.db_model.road_section import RoadSection


class Path(Base):
    __tablename__ = 'path'
    __table_args__ = (
        ForeignKeyConstraint(['navigation_id'], ['navigation.navigation_id'], ondelete='CASCADE', onupdate='CASCADE', name='path_ibfk_1'),
        Index('navigation_id', 'navigation_id'),
        Index('path_loc', 'path_loc')
    )

    path_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11))
    path_loc: Mapped[Point] = mapped_column(Point)
    distance: Mapped[int] = mapped_column(INTEGER(11))
    duration: Mapped[int] = mapped_column(INTEGER(11), comment='단위: ms (밀리초)')
    step_order: Mapped[int] = mapped_column(INTEGER(11))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation: Mapped['Navigation'] = relationship('Navigation', back_populates='path')
    road_section: Mapped[List['RoadSection']] = relationship('RoadSection', back_populates='path')
