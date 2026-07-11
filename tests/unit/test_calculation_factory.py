"""Unit tests for the calculation factory."""

import pytest

from app.operations.calculation_factory import (
    AddOperation,
    CalculationFactory,
    DivideOperation,
    MultiplyOperation,
    SubtractOperation,
)


@pytest.mark.parametrize(
    "calculation_type,a,b,expected",
    [
        ("Add", 10, 5, 15),
        ("Subtract", 10, 5, 5),
        ("Multiply", 10, 5, 50),
        ("Divide", 10, 5, 2),
    ],
)
def test_factory_calculates_supported_operations(
    calculation_type,
    a,
    b,
    expected,
):
    """The factory should perform every supported operation."""
    result = CalculationFactory.calculate(
        calculation_type,
        a,
        b,
    )

    assert result == expected


@pytest.mark.parametrize(
    "calculation_type,expected_class",
    [
        ("Add", AddOperation),
        ("Subtract", SubtractOperation),
        ("Multiply", MultiplyOperation),
        ("Divide", DivideOperation),
    ],
)
def test_factory_creates_correct_operation(
    calculation_type,
    expected_class,
):
    """The factory should return the correct operation object."""
    operation = CalculationFactory.create_operation(calculation_type)

    assert isinstance(operation, expected_class)


def test_factory_rejects_invalid_type():
    """Unsupported calculation types should raise an error."""
    with pytest.raises(
        ValueError,
        match="Unsupported calculation type",
    ):
        CalculationFactory.create_operation("Power")


def test_divide_rejects_zero_divisor():
    """Division by zero should raise a meaningful error."""
    with pytest.raises(
        ValueError,
        match="Cannot divide by zero",
    ):
        CalculationFactory.calculate("Divide", 10, 0)