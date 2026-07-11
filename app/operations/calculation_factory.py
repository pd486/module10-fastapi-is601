"""Factory classes for performing supported calculation operations."""

from abc import ABC, abstractmethod


class Operation(ABC):
    """Abstract base class for calculator operations."""

    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        """Calculate a result using two operands."""
        raise NotImplementedError  # pragma: no cover


class AddOperation(Operation):
    """Add two numbers."""

    def calculate(self, a: float, b: float) -> float:
        return a + b


class SubtractOperation(Operation):
    """Subtract the second number from the first."""

    def calculate(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(Operation):
    """Multiply two numbers."""

    def calculate(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(Operation):
    """Divide the first number by the second."""

    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class CalculationFactory:
    """Create the correct operation object from its type."""

    _operations = {
        "Add": AddOperation,
        "Subtract": SubtractOperation,
        "Multiply": MultiplyOperation,
        "Divide": DivideOperation,
    }

    @classmethod
    def create_operation(cls, calculation_type: str) -> Operation:
        """Return an operation object matching the requested type."""
        operation_class = cls._operations.get(calculation_type)

        if operation_class is None:
            raise ValueError(
                f"Unsupported calculation type: {calculation_type}"
            )

        return operation_class()

    @classmethod
    def calculate(
        cls,
        calculation_type: str,
        a: float,
        b: float,
    ) -> float:
        """Create the correct operation and return its result."""
        operation = cls.create_operation(calculation_type)
        return operation.calculate(a, b)