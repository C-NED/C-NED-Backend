from __future__ import annotations
from typing import Optional

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship

import datetime
from app.models.db_model.base import Base

class Guide(Base):
    __tablename__ = "guide"
    __table_args__ = (
        ForeignKeyConstraint(
            ["navigation_id"], ["navigation.navigation_id"],
            ondelete="CASCADE", onupdate="CASCADE", name="guide_ibfk_1"
        ),
        Index("idx_navigation_id", "navigation_id"),
        Index("idx_pointidx", "pointidx"),
    )

    guide_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    navigation_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    
    distance: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    duration: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    instructions: Mapped[str] = mapped_column(String(255), nullable=False)
    pointidx: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    step_order: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # 역방향 관계 (Navigation ↔ Guide)
    navigation_guide_from: Mapped["Navigation"] = relationship(
        "Navigation", back_populates="navigation_guide_to"
    )
