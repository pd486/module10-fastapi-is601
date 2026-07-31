"""Unit tests for the calculation factory."""

import pytest

from app.operations.calculation_factory import (
    AddOperation,
    CalculationFactory,
    DivideOperation,
    MultiplyOperation,
    PowerOperation,
    SubtractOperation,
)


@pytest.mark.parametrize(
    "calculation_type,a,b,expected",
    [
        ("Add", 10, 5, 15),
        ("Subtract", 10, 5, 5),
        ("Multiply", 10, 5, 50),
        ("Divide", 10, 5, 2),
        ("Power", 2, 10, 1024),
        ("Power", 5, 0, 1),
        ("Power", 4, 0.5, 2),
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
        ("Power", PowerOperation),
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
        CalculationFactory.create_operation("Modulus")


def test_divide_rejects_zero_divisor():
    """Division by zero should raise a meaningful error."""
    with pytest.raises(
        ValueError,
        match="Cannot divide by zero",
    ):
        CalculationFactory.calculate("Divide", 10, 0)


def test_power_rejects_zero_to_negative_power():
    """Zero raised to a negative power should raise a meaningful error."""
    with pytest.raises(
        ValueError,
        match="Cannot raise zero to a negative power",
    ):
        CalculationFactory.calculate("Power", 0, -1)


def test_power_rejects_negative_base_fractional_exponent():
    """A negative base with a fractional exponent has no real result."""
    with pytest.raises(
        ValueError,
        match="Cannot raise a negative number to a fractional power",
    ):
        CalculationFactory.calculate("Power", -8, 0.5)


def test_power_supports_negative_exponent():
    """A negative exponent should return the reciprocal power."""
    result = CalculationFactory.calculate("Power", 2, -2)

    assert result == 0.25


def test_power_supports_negative_base_with_integer_exponent():
    """A negative base with an integer exponent has a real result."""
    result = CalculationFactory.calculate("Power", -2, 3)

    assert result == -8
