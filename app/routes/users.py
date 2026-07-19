"""User registration and login routes."""

import traceback

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.base import UserCreate
from app.schemas.user import Token, UserLogin, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """Register a new user and securely hash the password."""
    try:
        new_user = User.register(
            db,
            user_data.model_dump(),
        )

        db.commit()
        db.refresh(new_user)

        return new_user

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        db.rollback()

        print("\nREGISTRATION ERROR")
        traceback.print_exc()
        print(f"ERROR TYPE: {type(exc).__name__}")
        print(f"ERROR MESSAGE: {exc}\n")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(exc).__name__}: {exc}",
        ) from exc


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """Authenticate a user and return a JWT access token."""
    try:
        token_data = User.authenticate(
            db,
            username=credentials.username,
            password=credentials.password,
        )

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={
                    "WWW-Authenticate": "Bearer",
                },
            )

        return token_data

    except HTTPException:
        raise

    except Exception as exc:
        db.rollback()

        print("\nLOGIN ERROR")
        traceback.print_exc()
        print(f"ERROR TYPE: {type(exc).__name__}")
        print(f"ERROR MESSAGE: {exc}\n")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{type(exc).__name__}: {exc}",
        ) from exc