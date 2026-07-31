"""Unit tests for calculation Pydantic schemas."""

import uuid

import pytest
from pydantic import ValidationError

from app.schemas.calculation import (
    CalculationCreate,
    CalculationRead,
    CalculationType,
)


@pytest.mark.parametrize(
    "calculation_type",
    [
        CalculationType.ADD,
        CalculationType.SUBTRACT,
        CalculationType.MULTIPLY,
        CalculationType.DIVIDE,
        CalculationType.POWER,
    ],
)
def test_calculation_create_accepts_valid_types(calculation_type):
    """CalculationCreate should accept each supported type."""
    calculation = CalculationCreate(
        a=10,
        b=5,
        type=calculation_type,
    )

    assert calculation.a == 10
    assert calculation.b == 5
    assert calculation.type == calculation_type


def test_calculation_create_rejects_invalid_type():
    """CalculationCreate should reject unsupported operation names."""
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10,
            b=5,
            type="Modulus",
        )


def test_calculation_create_rejects_division_by_zero():
    """A Divide calculation cannot use zero as the second operand."""
    with pytest.raises(
        ValidationError,
        match="Cannot divide by zero",
    ):
        CalculationCreate(
            a=10,
            b=0,
            type="Divide",
        )


def test_calculation_create_accepts_valid_power():
    """A Power calculation with a real-number result should validate."""
    calculation = CalculationCreate(
        a=2,
        b=10,
        type="Power",
    )

    assert calculation.type == CalculationType.POWER


def test_calculation_create_rejects_zero_to_negative_power():
    """A Power calculation cannot raise zero to a negative exponent."""
    with pytest.raises(
        ValidationError,
        match="Cannot raise zero to a negative power",
    ):
        CalculationCreate(
            a=0,
            b=-1,
            type="Power",
        )


def test_calculation_create_rejects_negative_base_fractional_power():
    """A Power calculation cannot use a negative base with a fractional exponent."""
    with pytest.raises(
        ValidationError,
        match="Cannot raise a negative number to a fractional power",
    ):
        CalculationCreate(
            a=-8,
            b=0.5,
            type="Power",
        )


def test_calculation_read_serializes_data():
    """CalculationRead should serialize a stored calculation record."""
    calculation_id = uuid.uuid4()

    calculation = CalculationRead(
        id=calculation_id,
        a=10,
        b=5,
        type=CalculationType.ADD,
        result=15,
    )

    assert calculation.id == calculation_id
    assert calculation.a == 10
    assert calculation.b == 5
    assert calculation.type == CalculationType.ADD
    assert calculation.result == 15
