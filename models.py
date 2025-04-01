from typing import Any, List, Optional

from sqlalchemy import BINARY, DateTime, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType
import datetime
from sqlalchemy.types import UserDefinedType


class Base(DeclarativeBase):
    pass

class Point(UserDefinedType):
    def get_col_spec(self, **kw):
        return "POINT"

    def bind_expression(self, bindvalue):
        return bindvalue

    def column_expression(self, col):
        return col


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


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    __table_args__ = (
        Index('idx_principal', 'principal_type', 'principal_id'),
        Index('refresh_token', 'refresh_token', unique=True)
    )

    refresh_token_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    principal_type: Mapped[str] = mapped_column(Enum('USER', 'ADMIN'))
    principal_id: Mapped[int] = mapped_column(INTEGER(11))
    refresh_token: Mapped[bytes] = mapped_column(BINARY(32))
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    revoked: Mapped[Optional[int]] = mapped_column(TINYINT(4), server_default=text('0'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))


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

    favorite_place: Mapped[List['FavoritePlace']] = relationship('FavoritePlace', back_populates='user')
    navigation: Mapped[List['Navigation']] = relationship('Navigation', back_populates='user')


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

    user: Mapped['User'] = relationship('User', back_populates='favorite_place')


class Navigation(Base):
    __tablename__ = 'navigation'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE', onupdate='CASCADE', name='navigation_ibfk_1'),
        Index('end_loc', 'end_loc'),
        Index('start_loc', 'start_loc'),
        Index('user_id', 'user_id')
    )

    navigation_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    user_id: Mapped[int] = mapped_column(INTEGER(11))
    start_loc: Mapped[Point] = mapped_column(Point)
    end_loc: Mapped[Point] = mapped_column(Point)
    arrival_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    road_option: Mapped[str] = mapped_column(Enum('trafast', 'tracomfort', 'traoptimal', 'traviodtoll', 'traavoidcaronly'))
    total_distance: Mapped[int] = mapped_column(INTEGER(11))
    total_time: Mapped[int] = mapped_column(INTEGER(11))
    taxifare: Mapped[int] = mapped_column(INTEGER(11))
    tollfare: Mapped[int] = mapped_column(INTEGER(11))
    fuelprice: Mapped[int] = mapped_column(INTEGER(11))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    user: Mapped['User'] = relationship('User', back_populates='navigation')
    caution: Mapped[List['Caution']] = relationship('Caution', back_populates='navigation')
    dangerous_incident: Mapped[List['DangerousIncident']] = relationship('DangerousIncident', back_populates='navigation')
    outbreak: Mapped[List['Outbreak']] = relationship('Outbreak', back_populates='navigation')
    path: Mapped[List['Path']] = relationship('Path', back_populates='navigation')
    vsl: Mapped[List['Vsl']] = relationship('Vsl', back_populates='navigation')
    road_section: Mapped[List['RoadSection']] = relationship('RoadSection', back_populates='navigation')


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
    principal_type: Mapped[str] = mapped_column(Enum('USER', 'ROAD_ADMIN'))
    message: Mapped[str] = mapped_column(String(100))
    loc: Mapped[Point] = mapped_column(Point)
    route_no: Mapped[str] = mapped_column(String(10))
    route_name: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation: Mapped['Navigation'] = relationship('Navigation', back_populates='caution')
    road_info: Mapped['RoadInfo'] = relationship('RoadInfo', back_populates='caution')


class DangerousIncident(Base):
    __tablename__ = 'dangerous_incident'
    __table_args__ = (
        ForeignKeyConstraint(['navigation_id'], ['navigation.navigation_id'], ondelete='CASCADE', onupdate='CASCADE', name='dangerous_incident_ibfk_1'),
        Index('navigation_id', 'navigation_id')
    )

    dincident_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_type: Mapped[str] = mapped_column(Enum('USER', 'ROAD_ADMIN'))
    loc: Mapped[Point] = mapped_column(Point)
    period: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation: Mapped['Navigation'] = relationship('Navigation', back_populates='dangerous_incident')


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
    principal_type: Mapped[str] = mapped_column(Enum('USER', 'ROAD_ADMIN'))
    event_type: Mapped[str] = mapped_column(String(10))
    period: Mapped[str] = mapped_column(String(15))
    road_name: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(String(100))
    loc: Mapped[Point] = mapped_column(Point)
    road_no: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation: Mapped['Navigation'] = relationship('Navigation', back_populates='outbreak')
    road_info: Mapped['RoadInfo'] = relationship('RoadInfo', back_populates='outbreak')


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


class Vsl(Base):
    __tablename__ = 'vsl'
    __table_args__ = (
        ForeignKeyConstraint(['navigation_id'], ['navigation.navigation_id'], ondelete='CASCADE', onupdate='CASCADE', name='vsl_ibfk_1'),
        ForeignKeyConstraint(['road_no'], ['road_info.road_no'], ondelete='CASCADE', onupdate='CASCADE', name='vsl_ibfk_2'),
        Index('navigation_id', 'navigation_id'),
        Index('road_no', 'road_no')
    )

    vsl_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_id: Mapped[int] = mapped_column(INTEGER(11))
    principal_type: Mapped[str] = mapped_column(Enum('USER', 'ROAD_ADMIN'))
    vsl_name: Mapped[str] = mapped_column(String(50))
    loc: Mapped[Point] = mapped_column(Point)
    registedDate: Mapped[str] = mapped_column(String(50))
    road_no: Mapped[str] = mapped_column(String(10))
    default_limit: Mapped[int] = mapped_column(INTEGER(11))
    cur_speed_limit_min: Mapped[int] = mapped_column(INTEGER(11))
    cur_speed_limit_max: Mapped[int] = mapped_column(INTEGER(11))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation: Mapped['Navigation'] = relationship('Navigation', back_populates='vsl')
    road_info: Mapped['RoadInfo'] = relationship('RoadInfo', back_populates='vsl')


class RoadSection(Base):
    __tablename__ = 'road_section'
    __table_args__ = (
        ForeignKeyConstraint(['navigation_id'], ['navigation.navigation_id'], ondelete='CASCADE', onupdate='CASCADE', name='road_section_ibfk_1'),
        ForeignKeyConstraint(['path_id'], ['path.path_id'], ondelete='CASCADE', onupdate='CASCADE', name='road_section_ibfk_2'),
        Index('navigation_id', 'navigation_id'),
        Index('path_id', 'path_id')
    )

    road_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11))
    path_id: Mapped[int] = mapped_column(INTEGER(11))
    name: Mapped[str] = mapped_column(String(30))
    distance: Mapped[int] = mapped_column(INTEGER(11))
    speed: Mapped[int] = mapped_column(INTEGER(11))
    congestion: Mapped[str] = mapped_column(Enum('정보 없음', '원활', '서행', '혼잡'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('current_timestamp() ON UPDATE current_timestamp()'))

    navigation: Mapped['Navigation'] = relationship('Navigation', back_populates='road_section')
    path: Mapped['Path'] = relationship('Path', back_populates='road_section')
