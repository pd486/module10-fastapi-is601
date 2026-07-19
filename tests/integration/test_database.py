"""Integration tests for database helpers."""

from unittest.mock import patch

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_engine, get_sessionmaker


def test_base_declaration():
    """Verify that the shared SQLAlchemy Base is available."""

    assert Base is not None
    assert hasattr(Base, "metadata")


def test_get_engine_success():
    """Verify that get_engine returns a SQLAlchemy engine."""

    engine = get_engine(
        database_url="postgresql://user:password@localhost:5432/mytestdb"
    )

    try:
        assert isinstance(engine, Engine)
    finally:
        engine.dispose()


def test_get_engine_failure():
    """Verify that engine creation errors are propagated."""

    with patch(
        "app.database.create_engine",
        side_effect=SQLAlchemyError("Engine error"),
    ):
        with pytest.raises(SQLAlchemyError, match="Engine error"):
            get_engine(
                database_url=(
                    "postgresql://user:password@localhost:5432/mytestdb"
                )
            )


def test_get_sessionmaker():
    """Verify that get_sessionmaker returns a session factory."""

    engine = get_engine(
        database_url="postgresql://user:password@localhost:5432/mytestdb"
    )

    try:
        session_factory = get_sessionmaker(engine=engine)
        assert isinstance(session_factory, sessionmaker)
    finally:
        engine.dispose()
