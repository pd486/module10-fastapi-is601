"""Integration tests for the /calculations HTTP routes, including Power."""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Provide a TestClient bound to the real FastAPI app and database."""

    with TestClient(app) as test_client:
        yield test_client


def test_create_power_calculation_via_api(client, db_session):
    """POST /calculations should store a Power calculation and return it."""

    response = client.post(
        "/calculations",
        json={"a": 2, "b": 10, "type": "Power"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["a"] == 2
    assert data["b"] == 10
    assert data["type"] == "Power"
    assert data["result"] == 1024
    assert "id" in data


def test_create_power_calculation_persists_and_is_readable(client, db_session):
    """A created Power calculation should be retrievable via GET."""

    create_response = client.post(
        "/calculations",
        json={"a": 3, "b": 3, "type": "Power"},
    )
    assert create_response.status_code == 201

    calculation_id = create_response.json()["id"]

    read_response = client.get(f"/calculations/{calculation_id}")

    assert read_response.status_code == 200
    assert read_response.json()["result"] == 27
    assert read_response.json()["type"] == "Power"


def test_create_power_calculation_rejects_zero_to_negative_power(
    client,
    db_session,
):
    """POST /calculations should reject an invalid Power calculation."""

    response = client.post(
        "/calculations",
        json={"a": 0, "b": -1, "type": "Power"},
    )

    assert response.status_code == 400
    assert "Cannot raise zero to a negative power" in response.json()["error"]


def test_update_calculation_to_power_recomputes_result(client, db_session):
    """PUT /calculations/{id} should recompute the result for Power."""

    create_response = client.post(
        "/calculations",
        json={"a": 10, "b": 5, "type": "Add"},
    )
    assert create_response.status_code == 201

    calculation_id = create_response.json()["id"]

    update_response = client.put(
        f"/calculations/{calculation_id}",
        json={"a": 2, "b": 5, "type": "Power"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["type"] == "Power"
    assert update_response.json()["result"] == 32
