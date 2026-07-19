import pytest
from uuid import uuid4

from app.models.user import User


def unique_user_data():
    token = uuid4().hex

    return {
        "first_name": "Test",
        "last_name": "User",
        "email": f"user_{token}@example.com",
        "username": f"user_{token}",
        "password": "TestPass123",
    }


def test_password_hashing(db_session, fake_user_data):
    """Test password hashing and verification functionality"""
    original_password = "TestPass123"
    hashed = User.hash_password(original_password)

    token = uuid4().hex

    user = User(
        first_name=fake_user_data["first_name"],
        last_name=fake_user_data["last_name"],
        email=f"hash_{token}@example.com",
        username=f"hash_{token}",
        password=hashed,
    )

    assert user.verify_password(original_password) is True
    assert user.verify_password("WrongPass123") is False
    assert hashed != original_password


def test_user_registration(db_session):
    """Test user registration process"""
    user_data = unique_user_data()

    user = User.register(db_session, user_data)
    db_session.commit()
    db_session.refresh(user)

    assert user.first_name == user_data["first_name"]
    assert user.last_name == user_data["last_name"]
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.is_active is True
    assert user.is_verified is False
    assert user.verify_password("TestPass123") is True


def test_duplicate_user_registration(db_session):
    """Test registration with duplicate email"""
    user1 = unique_user_data()
    user2 = unique_user_data()

    user2["email"] = user1["email"]

    first_user = User.register(db_session, user1)
    db_session.commit()
    db_session.refresh(first_user)

    with pytest.raises(ValueError, match="Username or email already exists"):
        User.register(db_session, user2)


def test_user_authentication(db_session):
    """Test user authentication"""
    user_data = unique_user_data()

    User.register(db_session, user_data)
    db_session.commit()

    auth_result = User.authenticate(
        db_session,
        user_data["username"],
        "TestPass123",
    )

    assert auth_result is not None
    assert "access_token" in auth_result
    assert auth_result["token_type"] == "bearer"
    assert "user" in auth_result


def test_user_last_login_update(db_session):
    """Test last_login update"""
    user_data = unique_user_data()

    user = User.register(db_session, user_data)
    db_session.commit()

    assert user.last_login is None

    User.authenticate(
        db_session,
        user_data["username"],
        "TestPass123",
    )

    db_session.refresh(user)

    assert user.last_login is not None


def test_unique_email_username(db_session):
    """Test duplicate email rejection"""
    user1 = unique_user_data()
    user2 = unique_user_data()

    user2["email"] = user1["email"]

    User.register(db_session, user1)
    db_session.commit()

    with pytest.raises(ValueError, match="Username or email already exists"):
        User.register(db_session, user2)


def test_short_password_registration(db_session):
    """Short passwords should fail."""
    user_data = unique_user_data()
    user_data["password"] = "Shor1"

    with pytest.raises(ValueError, match="Password must be at least 6 characters long"):
        User.register(db_session, user_data)


def test_invalid_token():
    """Invalid JWT returns None."""
    assert User.verify_token("invalid.token.string") is None


def test_token_creation_and_verification(db_session):
    """Token creation and verification"""
    user_data = unique_user_data()

    user = User.register(db_session, user_data)
    db_session.commit()

    token = User.create_access_token({"sub": str(user.id)})

    assert User.verify_token(token) == user.id


def test_authenticate_with_email(db_session):
    """Authenticate using email"""
    user_data = unique_user_data()

    User.register(db_session, user_data)
    db_session.commit()

    auth_result = User.authenticate(
        db_session,
        user_data["email"],
        "TestPass123",
    )

    assert auth_result is not None
    assert "access_token" in auth_result


def test_user_model_representation(test_user):
    """String representation"""
    expected = (
        f"<User(username={test_user.username}, "
        f"email={test_user.email})>"
    )

    assert str(test_user) == expected


def test_missing_password_registration(db_session):
    """Missing password should fail."""
    token = uuid4().hex

    test_data = {
        "first_name": "NoPassword",
        "last_name": "Test",
        "email": f"nopass_{token}@example.com",
        "username": f"nopass_{token}",
    }

    with pytest.raises(ValueError, match="Field required"):
        User.register(db_session, test_data)