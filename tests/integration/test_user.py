"""Integration tests for the User model and database sessions."""

from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from tests.conftest import create_fake_user, managed_db_session


def unique_value(prefix: str) -> str:
    """Return a value that remains unique across tests and previous runs."""
    return f"{prefix}_{uuid4().hex}"


def create_unique_user_data() -> dict:
    """Create user data guaranteed to be unique across repeated test runs."""
    token = uuid4().hex

    return {
        "first_name": "Test",
        "last_name": "User",
        "email": f"user_{token}@example.com",
        "username": f"user_{token}",
        "password": "password123",
    }


def test_database_connection(db_session):
    """Verify that the database connection works."""
    result = db_session.execute(text("SELECT 1"))

    assert result.scalar() == 1


def test_managed_session():
    """Verify that managed_db_session provides a working session."""
    with managed_db_session() as session:
        result = session.execute(text("SELECT 1"))

        assert result.scalar() == 1


def test_session_handling(db_session):
    """Verify commit, constraint failure, rollback, and continued session use."""
    initial_count = db_session.query(User).count()

    first_data = create_unique_user_data()
    first_user = User(**first_data)

    db_session.add(first_user)
    db_session.commit()
    db_session.refresh(first_user)

    assert first_user.id is not None
    assert db_session.query(User).count() == initial_count + 1

    duplicate_data = create_unique_user_data()
    duplicate_data["email"] = first_data["email"]

    duplicate_user = User(**duplicate_data)
    db_session.add(duplicate_user)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    persisted_first_user = (
        db_session.query(User)
        .filter_by(email=first_data["email"])
        .first()
    )

    assert persisted_first_user is not None
    assert persisted_first_user.id == first_user.id

    third_data = create_unique_user_data()
    third_user = User(**third_data)

    db_session.add(third_user)
    db_session.commit()
    db_session.refresh(third_user)

    created_users = (
        db_session.query(User)
        .filter(User.id.in_([first_user.id, third_user.id]))
        .all()
    )

    assert len(created_users) == 2
    assert {user.id for user in created_users} == {
        first_user.id,
        third_user.id,
    }
    assert db_session.query(User).count() == initial_count + 2


def test_create_user_with_faker(db_session):
    """Create and persist one Faker-generated user."""
    user_data = create_fake_user()

    token = uuid4().hex
    user_data["email"] = f"faker_{token}@example.com"
    user_data["username"] = f"faker_{token}"

    user = User(**user_data)

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]


def test_create_multiple_users(db_session):
    """Create three unique users and verify persistence."""
    initial_count = db_session.query(User).count()

    users = [
        User(**create_unique_user_data())
        for _ in range(3)
    ]

    db_session.add_all(users)
    db_session.commit()

    for user in users:
        db_session.refresh(user)

    persisted_ids = {
        user.id
        for user in db_session.query(User)
        .filter(User.id.in_([user.id for user in users]))
        .all()
    }

    assert len(users) == 3
    assert all(user.id is not None for user in users)
    assert persisted_ids == {user.id for user in users}
    assert db_session.query(User).count() == initial_count + 3


def test_query_methods(db_session):
    """Verify filtering, counting, and ordering using test-owned records."""
    users = [
        User(**create_unique_user_data())
        for _ in range(5)
    ]

    db_session.add_all(users)
    db_session.commit()

    for user in users:
        db_session.refresh(user)

    user_ids = [user.id for user in users]
    expected_emails = sorted(user.email for user in users)

    persisted_users = (
        db_session.query(User)
        .filter(User.id.in_(user_ids))
        .all()
    )

    assert len(persisted_users) == 5
    assert {user.id for user in persisted_users} == set(user_ids)

    first_user = users[0]

    found_user = (
        db_session.query(User)
        .filter_by(email=first_user.email)
        .first()
    )

    assert found_user is not None
    assert found_user.id == first_user.id

    ordered_users = (
        db_session.query(User)
        .filter(User.id.in_(user_ids))
        .order_by(User.email)
        .all()
    )

    assert [user.email for user in ordered_users] == expected_emails


def test_transaction_rollback(db_session):
    """Verify that rollback removes an uncommitted user."""
    user = User(**create_unique_user_data())

    db_session.add(user)
    db_session.flush()

    user_id = user.id

    assert (
        db_session.query(User)
        .filter_by(id=user_id)
        .first()
        is not None
    )

    db_session.rollback()

    assert (
        db_session.query(User)
        .filter_by(id=user_id)
        .first()
        is None
    )


def test_update_with_refresh(db_session):
    """Update a persisted user and verify the refreshed value."""
    user = User(**create_unique_user_data())

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    new_email = f"updated_{uuid4().hex}@example.com"
    user.email = new_email

    db_session.commit()
    db_session.refresh(user)

    assert user.email == new_email


@pytest.mark.slow
def test_bulk_operations(db_session):
    """Insert ten unique users in one operation."""
    initial_count = db_session.query(User).count()

    users = [
        User(**create_unique_user_data())
        for _ in range(10)
    ]

    db_session.add_all(users)
    db_session.commit()

    inserted_ids = [user.id for user in users]

    persisted_count = (
        db_session.query(User)
        .filter(User.id.in_(inserted_ids))
        .count()
    )

    assert persisted_count == 10
    assert db_session.query(User).count() == initial_count + 10


def test_unique_email_constraint(db_session):
    """Verify that duplicate email addresses are rejected."""
    first_data = create_unique_user_data()
    first_user = User(**first_data)

    db_session.add(first_user)
    db_session.commit()
    db_session.refresh(first_user)

    duplicate_data = create_unique_user_data()
    duplicate_data["email"] = first_data["email"]

    duplicate_user = User(**duplicate_data)
    db_session.add(duplicate_user)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    matching_users = (
        db_session.query(User)
        .filter_by(email=first_data["email"])
        .all()
    )

    assert len(matching_users) == 1
    assert matching_users[0].id == first_user.id


def test_unique_username_constraint(db_session):
    """Verify that duplicate usernames are rejected."""
    first_data = create_unique_user_data()
    first_user = User(**first_data)

    db_session.add(first_user)
    db_session.commit()
    db_session.refresh(first_user)

    duplicate_data = create_unique_user_data()
    duplicate_data["username"] = first_data["username"]

    duplicate_user = User(**duplicate_data)
    db_session.add(duplicate_user)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    matching_users = (
        db_session.query(User)
        .filter_by(username=first_data["username"])
        .all()
    )

    assert len(matching_users) == 1
    assert matching_users[0].id == first_user.id


def test_user_persistence_after_constraint(db_session):
    """Verify that a committed user survives a failed duplicate insert."""
    original_data = create_unique_user_data()
    original_user = User(**original_data)

    db_session.add(original_user)
    db_session.commit()
    db_session.refresh(original_user)

    saved_id = original_user.id

    duplicate_data = create_unique_user_data()
    duplicate_data["email"] = original_data["email"]

    duplicate_user = User(**duplicate_data)
    db_session.add(duplicate_user)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    persisted_user = (
        db_session.query(User)
        .filter_by(id=saved_id)
        .first()
    )

    assert persisted_user is not None
    assert persisted_user.id == saved_id
    assert persisted_user.email == original_data["email"]
    assert persisted_user.username == original_data["username"]


def test_error_handling():
    """Verify that invalid SQL errors propagate from managed sessions."""
    with pytest.raises(Exception):
        with managed_db_session() as session:
            session.execute(text("INVALID SQL"))