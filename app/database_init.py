"""Create or remove application database tables."""

from app.database import engine
from app.models.user import Base, User
from app.models.calculation import Calculation


def init_db():
    """Create all registered SQLAlchemy tables."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all registered SQLAlchemy tables."""
    Base.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    init_db()
