"""Pydantic schemas for calculation validation and serialization."""

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class CalculationType(str, Enum):
    """Allowed calculation operation types."""

    ADD = "Add"
    SUBTRACT = "Subtract"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"
    POWER = "Power"


class CalculationCreate(BaseModel):
    """Validate data used to create a calculation."""

    a: float
    b: float
    type: CalculationType

    @model_validator(mode="after")
    def validate_division(self) -> "CalculationCreate":
        """Reject division by zero."""
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self

    @model_validator(mode="after")
    def validate_power(self) -> "CalculationCreate":
        """Reject power operations with no real-number result."""
        if self.type == CalculationType.POWER:
            if self.a == 0 and self.b < 0:
                raise ValueError("Cannot raise zero to a negative power")

            if self.a < 0 and not float(self.b).is_integer():
                raise ValueError(
                    "Cannot raise a negative number to a fractional power"
                )

        return self


class CalculationRead(BaseModel):
    """Serialize stored calculation data."""

    id: UUID
    a: float
    b: float
    type: CalculationType
    result: float

    model_config = ConfigDict(from_attributes=True)
