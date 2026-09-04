"""
InsightPilot AI — Declarative Database Base
SQLAlchemy 2.0 Base model with common columns and utility methods.
"""

from datetime import datetime
from typing import Any, Dict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def to_dict(self) -> Dict[str, Any]:
        """Converts model instance columns to a dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
