"""Calculation BREAD routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.calculation import Calculation
from app.operations.calculation_factory import CalculationFactory
from app.schemas.calculation import CalculationCreate, CalculationRead


router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
)


@router.get("", response_model=list[CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    """Browse all stored calculations."""
    return db.query(Calculation).order_by(Calculation.created_at.desc()).all()


@router.get("/{calculation_id}", response_model=CalculationRead)
def read_calculation(
    calculation_id: UUID,
    db: Session = Depends(get_db),
):
    """Read one calculation by ID."""
    calculation = (
        db.query(Calculation)
        .filter(Calculation.id == calculation_id)
        .first()
    )

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    return calculation


@router.post(
    "",
    response_model=CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def add_calculation(
    calculation_data: CalculationCreate,
    db: Session = Depends(get_db),
):
    """Add and store a new calculation."""
    calculation_type = calculation_data.type.value

    try:
        result = CalculationFactory.calculate(
            calculation_type=calculation_type,
            a=calculation_data.a,
            b=calculation_data.b,
        )

        calculation = Calculation(
            a=calculation_data.a,
            b=calculation_data.b,
            type=calculation_type,
            result=result,
        )

        db.add(calculation)
        db.commit()
        db.refresh(calculation)
        return calculation
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create calculation",
        ) from exc


@router.put("/{calculation_id}", response_model=CalculationRead)
def edit_calculation(
    calculation_id: UUID,
    calculation_data: CalculationCreate,
    db: Session = Depends(get_db),
):
    """Edit an existing calculation and recompute its result."""
    calculation = (
        db.query(Calculation)
        .filter(Calculation.id == calculation_id)
        .first()
    )

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    calculation_type = calculation_data.type.value

    try:
        calculation.a = calculation_data.a
        calculation.b = calculation_data.b
        calculation.type = calculation_type
        calculation.result = CalculationFactory.calculate(
            calculation_type=calculation_type,
            a=calculation_data.a,
            b=calculation_data.b,
        )

        db.commit()
        db.refresh(calculation)
        return calculation
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update calculation",
        ) from exc


@router.delete(
    "/{calculation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_calculation(
    calculation_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete one calculation by ID."""
    calculation = (
        db.query(Calculation)
        .filter(Calculation.id == calculation_id)
        .first()
    )

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    db.delete(calculation)
    db.commit()
    return None
