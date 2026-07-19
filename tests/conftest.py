import logging
import subprocess
import time
from contextlib import contextmanager
from typing import Dict, Generator, List
from uuid import uuid4

import pytest
import requests
from faker import Faker
from playwright.sync_api import Browser, Page, sync_playwright
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, get_engine, get_sessionmaker
from app.models.user import User


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

fake = Faker()
Faker.seed(12345)

test_engine = get_engine(database_url=settings.DATABASE_URL)
TestingSessionLocal = get_sessionmaker(engine=test_engine)


def create_fake_user() -> Dict[str, str]:
    """Generate fake user data with guaranteed unique identifiers."""

    unique_token = uuid4().hex

    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": f"user_{unique_token}@example.com",
        "username": f"user_{unique_token}",
        "password": fake.password(length=12),
    }


def clean_database(session: Session) -> None:
    """Rollback the current transaction and delete all table data."""

    session.rollback()

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())

    session.commit()


@contextmanager
def managed_db_session():
    """Provide a standalone database session with rollback handling."""

    session = TestingSessionLocal()

    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def wait_for_server(url: str, timeout: int = 30) -> bool:
    """Wait for the FastAPI server to respond."""

    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)

            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass

        time.sleep(1)

    return False


class ServerStartupError(Exception):
    """Raised when the FastAPI test server cannot be started."""


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(request):
    """Create a clean test schema before the suite."""

    preserve_db = request.config.getoption("--preserve-db")

    logger.info("Creating clean test database schema.")

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    if preserve_db:
        logger.info(
            "Preserving database because --preserve-db was supplied."
        )
    else:
        logger.info("Dropping test database schema.")
        Base.metadata.drop_all(bind=test_engine)

    test_engine.dispose()


@pytest.fixture
def db_session(request) -> Generator[Session, None, None]:
    """Provide an isolated database session for each test."""

    session = TestingSessionLocal()
    preserve_db = request.config.getoption("--preserve-db")

    try:
        Base.metadata.create_all(bind=test_engine)

        if not preserve_db:
            clean_database(session)

        yield session
    finally:
        try:
            session.rollback()

            if not preserve_db:
                clean_database(session)
        finally:
            session.close()


@pytest.fixture
def fake_user_data() -> Dict[str, str]:
    """Provide fake user data with unique email and username values."""

    return create_fake_user()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create and return one persisted user."""

    user = User(**create_fake_user())

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def seed_users(
    db_session: Session,
    request,
) -> List[User]:
    """Create several persisted test users."""

    number_of_users = getattr(request, "param", 5)

    users = [
        User(**create_fake_user())
        for _ in range(number_of_users)
    ]

    db_session.add_all(users)
    db_session.commit()

    for user in users:
        db_session.refresh(user)

    return users


@pytest.fixture(scope="session")
def fastapi_server():
    """Start and stop the FastAPI server for browser tests."""

    server_url = "http://127.0.0.1:8000/"

    process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        if not wait_for_server(server_url):
            raise ServerStartupError(
                "FastAPI server failed to start."
            )

        yield server_url
    finally:
        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


@pytest.fixture(scope="session")
def browser_context():
    """Provide a Playwright browser."""

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def page(
    browser_context: Browser,
) -> Generator[Page, None, None]:
    """Provide a fresh browser page for each UI test."""

    context = browser_context.new_context(
        viewport={
            "width": 1920,
            "height": 1080,
        },
        ignore_https_errors=True,
    )

    browser_page = context.new_page()

    try:
        yield browser_page
    finally:
        browser_page.close()
        context.close()


def pytest_addoption(parser):
    """Register custom pytest command-line options."""

    parser.addoption(
        "--preserve-db",
        action="store_true",
        default=False,
        help="Preserve the database after tests.",
    )

    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="Run tests marked as slow.",
    )


def pytest_collection_modifyitems(config, items):
    """Skip slow tests unless --run-slow is supplied."""

    if config.getoption("--run-slow"):
        return

    skip_slow = pytest.mark.skip(
        reason="Use --run-slow to run this test."
    )

    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)