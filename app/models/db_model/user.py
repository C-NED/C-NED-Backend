from __future__ import annotations
from typing import Any, List, Optional
from sqlalchemy import DateTime, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from app.models.db_model.base import Base
# from app.models.db_model.favorite_place import FavoritePlace
# from app.models.db_model.navigation import Navigation
# from app.models.db_model.vsl import Vsl
# from app.models.db_model.caution import Caution
# from app.models.db_model.dangerous_incident import DangerousIncident
# from app.models.db_model.outbreak import Outbreak
from app.auth.relationships import user_navigation_join,user_caution_join,user_dangerous_join,user_outbreak_join,user_vsl_join,user_refresh_join


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        Index('email', 'email', unique=True),
    )

    user_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    naver_auth: Mapped[int] = mapped_column(TINYINT(1))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    user_favorite_place_to: Mapped[List['FavoritePlace']] = relationship('FavoritePlace', back_populates='user_favorite_place_from')

    #다형성 fk 정의

    user_navigation_to: Mapped[List['Navigation']] = relationship(
        'Navigation',
        primaryjoin=lambda:user_navigation_join(),
        back_populates='user_navigation_from',
        lazy='select',
        viewonly=True
    )

    user_outbreak_to: Mapped[List['Outbreak']] = relationship(
        'Outbreak',
        primaryjoin=user_outbreak_join,
        back_populates='user_outbreak_from',
        viewonly=True,
        lazy='select'
    )

    user_vsl_to: Mapped[List['Vsl']] = relationship(
        'Vsl',
        primaryjoin=user_vsl_join,
        back_populates='user_vsl_from',
        viewonly=True,
        lazy='select'
    )

    user_caution_to: Mapped[List['Caution']] = relationship(
        'Caution',
        primaryjoin=user_caution_join,
        back_populates='user_caution_from',
        viewonly=True,
        lazy='select'
    )

    user_dangerous_incident_to: Mapped[List['DangerousIncident']] = relationship(
        'DangerousIncident',
        primaryjoin=user_dangerous_join,
        back_populates='user_dangerous_incident_from',
        viewonly=True,
        lazy='select'
    )

    user_refresh_to : Mapped[List['RefreshToken']] = relationship(
        'RefreshToken',
        primaryjoin=user_refresh_join,
        back_populates='user_refresh_from',
        viewonly=True,
        lazy='select'
    )
