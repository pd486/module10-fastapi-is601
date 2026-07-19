"""User database model and authentication helpers."""

from datetime import datetime, timedelta
import uuid
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

from app.schemas.base import UserCreate
from app.schemas.user import Token, UserResponse



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(Base):
    """Database model for application users."""

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    first_name = Column(
        String(50),
        nullable=False,
    )

    last_name = Column(
        String(50),
        nullable=False,
    )

    email = Column(
        String(120),
        unique=True,
        nullable=False,
        index=True,
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    password = Column(
        String(255),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"<User("
            f"username={self.username}, "
            f"email={self.email}"
            f")>"
        )

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain-text password using bcrypt."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        """Verify a plain-text password against the stored hash."""
        return pwd_context.verify(
            plain_password,
            self.password,
        )

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Create a signed JWT access token."""
        token_data = data.copy()

        expiration = datetime.utcnow() + (
            expires_delta
            or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        token_data.update(
            {
                "exp": expiration,
            }
        )

        return jwt.encode(
            token_data,
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

    @staticmethod
    def verify_token(token: str) -> Optional[uuid.UUID]:
        """Validate a JWT and return the user UUID."""
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
            )

            user_id = payload.get("sub")

            if not user_id:
                return None

            return uuid.UUID(user_id)

        except (JWTError, ValueError, TypeError):
            return None

    @classmethod
    def register(
        cls,
        db,
        user_data: Dict[str, Any],
    ) -> "User":
        """Validate registration data and create a new user."""
        try:
            validated_user = UserCreate.model_validate(user_data)

            existing_user = (
                db.query(cls)
                .filter(
                    (cls.email == validated_user.email)
                    | (cls.username == validated_user.username)
                )
                .first()
            )

            if existing_user:
                raise ValueError(
                    "Username or email already exists"
                )

            new_user = cls(
                first_name=validated_user.first_name,
                last_name=validated_user.last_name,
                email=validated_user.email,
                username=validated_user.username,
                password=cls.hash_password(
                    validated_user.password
                ),
                is_active=True,
                is_verified=False,
            )

            db.add(new_user)
            db.flush()

            return new_user

        except ValidationError as exc:
            raise ValueError(str(exc)) from exc

    @classmethod
    def authenticate(
        cls,
        db,
        username: str,
        password: str,
    ) -> Optional[Dict[str, Any]]:
        """Authenticate a user and return token response data."""
        user = (
            db.query(cls)
            .filter(
                (cls.username == username)
                | (cls.email == username)
            )
            .first()
        )

        if user is None:
            return None

        if not user.verify_password(password):
            return None

        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)

        user_response = UserResponse.model_validate(user)

        token_response = Token(
            access_token=cls.create_access_token(
                {
                    "sub": str(user.id),
                }
            ),
            token_type="bearer",
            user=user_response,
        )

        return token_response.model_dump()