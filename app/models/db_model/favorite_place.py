from __future__ import annotations

from typing import Optional
from sqlalchemy import DateTime, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
from app.models.db_model.types.point import Point
# from app.models.db_model.user import User

class FavoritePlace(Base):
    __tablename__ = 'favorite_place'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE', onupdate='CASCADE', name='favorite_place_ibfk_1'),
        Index('loc', 'loc'),
        Index('user_id_idx', 'user_id')
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    user_id: Mapped[int] = mapped_column(INTEGER(11))
    loc: Mapped[Point] = mapped_column(Point)
    name: Mapped[str] = mapped_column(String(30))
    addr: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    user_favorite_place_from: Mapped['User'] = relationship('User', back_populates='user_favorite_place_to')
