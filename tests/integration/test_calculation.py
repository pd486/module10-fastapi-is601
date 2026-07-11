"""Integration tests for the SQLAlchemy Calculation model."""

from app.models.calculation import Calculation
from app.operations.calculation_factory import CalculationFactory


def test_create_calculation_record(db_session):
    """A calculation should be stored and retrieved from PostgreSQL."""

    result = CalculationFactory.calculate(
        "Add",
        10,
        5,
    )

    calculation = Calculation(
        a=10,
        b=5,
        type="Add",
        result=result,
    )

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    stored_calculation = (
        db_session.query(Calculation)
        .filter(Calculation.id == calculation.id)
        .first()
    )

    assert stored_calculation is not None
    assert stored_calculation.a == 10
    assert stored_calculation.b == 5
    assert stored_calculation.type == "Add"
    assert stored_calculation.result == 15
    assert stored_calculation.created_at is not None


def test_store_division_calculation(db_session):
    """A valid division calculation should be stored correctly."""

    result = CalculationFactory.calculate(
        "Divide",
        20,
        4,
    )

    calculation = Calculation(
        a=20,
        b=4,
        type="Divide",
        result=result,
    )

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    assert calculation.id is not None
    assert calculation.result == 5