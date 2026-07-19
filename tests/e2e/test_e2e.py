# tests/e2e/test_e2e.py

"""Playwright E2E tests for Module 13 authentication."""

from uuid import uuid4

import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:8000"


def create_unique_user() -> dict[str, str]:
    """Return unique valid user data for an E2E test."""

    unique_id = uuid4().hex[:10]

    return {
        "username": f"user_{unique_id}",
        "email": f"user_{unique_id}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password1",
    }


def register_user(page: Page, user: dict[str, str]) -> None:
    """Register a user through the browser interface."""

    page.goto(f"{BASE_URL}/register")

    page.fill("#username", user["username"])
    page.fill("#email", user["email"])
    page.fill("#first_name", user["first_name"])
    page.fill("#last_name", user["last_name"])
    page.fill("#password", user["password"])
    page.fill("#confirm_password", user["password"])

    page.click("#registerButton")


@pytest.mark.e2e
def test_successful_registration(
    page: Page,
    fastapi_server,
) -> None:
    """A user can register with valid information."""

    user = create_unique_user()

    register_user(page, user)

    success_message = page.locator("#successMessage")

    expect(success_message).to_be_visible()
    expect(success_message).to_have_text(
        "Registration successful! Redirecting to login..."
    )


@pytest.mark.e2e
def test_successful_login_stores_jwt(
    page: Page,
    fastapi_server,
) -> None:
    """A registered user can log in and store a JWT in localStorage."""

    user = create_unique_user()

    register_user(page, user)

    expect(page.locator("#successMessage")).to_have_text(
        "Registration successful! Redirecting to login..."
    )

    page.goto(f"{BASE_URL}/login")

    page.fill("#username", user["username"])
    page.fill("#password", user["password"])
    page.click("#loginButton")

    success_message = page.locator("#successMessage")

    expect(success_message).to_be_visible()
    expect(success_message).to_have_text(
        "Login successful! JWT token stored."
    )

    access_token = page.evaluate(
        "() => localStorage.getItem('access_token')"
    )
    token_type = page.evaluate(
        "() => localStorage.getItem('token_type')"
    )

    assert access_token is not None
    assert access_token != ""
    assert token_type == "bearer"


@pytest.mark.e2e
def test_registration_rejects_short_password(
    page: Page,
    fastapi_server,
) -> None:
    """The registration page rejects a short, weak password."""

    user = create_unique_user()

    page.goto(f"{BASE_URL}/register")

    page.fill("#username", user["username"])
    page.fill("#email", user["email"])
    page.fill("#first_name", user["first_name"])
    page.fill("#last_name", user["last_name"])
    page.fill("#password", "abc")
    page.fill("#confirm_password", "abc")

    page.click("#registerButton")

    error_message = page.locator("#errorMessage")

    expect(error_message).to_be_visible()
    expect(error_message).to_have_text(
        "Password must be at least 6 characters long and contain "
        "uppercase, lowercase, and a number"
    )

    expect(page.locator("#successAlert")).to_be_hidden()


@pytest.mark.e2e
def test_login_rejects_incorrect_password(
    page: Page,
    fastapi_server,
) -> None:
    """The login page displays an error for an incorrect password."""

    user = create_unique_user()

    register_user(page, user)

    expect(page.locator("#successMessage")).to_have_text(
        "Registration successful! Redirecting to login..."
    )

    page.goto(f"{BASE_URL}/login")

    page.fill("#username", user["username"])
    page.fill("#password", "WrongPassword1")
    page.click("#loginButton")

    error_message = page.locator("#errorMessage")

    expect(error_message).to_be_visible()
    expect(error_message).to_have_text(
        "Invalid username or password"
    )

    access_token = page.evaluate(
        "() => localStorage.getItem('access_token')"
    )

    assert access_token is None