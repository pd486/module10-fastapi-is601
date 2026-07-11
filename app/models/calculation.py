"""SQLAlchemy model for stored calculator calculations."""

from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID

from app.models.user import Base


class Calculation(Base):
    """Store one calculation in the database."""

    __tablename__ = "calculations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(String(20), nullable=False)
    result = Column(Float, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"<Calculation(type={self.type}, "
            f"a={self.a}, b={self.b}, result={self.result})>"
        )