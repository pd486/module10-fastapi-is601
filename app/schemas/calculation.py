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


class CalculationRead(BaseModel):
    """Serialize stored calculation data."""

    id: UUID
    a: float
    b: float
    type: CalculationType
    result: float

    model_config = ConfigDict(from_attributes=True)
    