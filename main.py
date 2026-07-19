# main.py

import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator

from app.operations import add, divide, multiply, subtract
from app.routes.calculations import router as calculations_router
from app.routes.users import router as users_router


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create FastAPI application
app = FastAPI(
    title="FastAPI Calculator",
    description="Calculator application with JWT authentication",
    version="13.0.0",
)


# Include API routers
app.include_router(users_router)
app.include_router(calculations_router)


# Configure front-end files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class OperationRequest(BaseModel):
    """Request model for calculator operations."""

    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator("a", "b")
    @classmethod
    def validate_numbers(cls, value: float) -> float:
        if not isinstance(value, (int, float)):
            raise ValueError("Both a and b must be numbers.")
        return value


class OperationResponse(BaseModel):
    """Response model for successful calculator operations."""

    result: float = Field(..., description="The result of the operation")


class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str = Field(..., description="Error message")


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """Return API errors in a consistent JSON format."""

    logger.error("HTTPException on %s: %s", request.url.path, exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return request-validation errors in a consistent format."""

    error_messages = "; ".join(
        f"{error['loc'][-1]}: {error['msg']}"
        for error in exc.errors()
    )

    logger.error(
        "ValidationError on %s: %s",
        request.url.path,
        error_messages,
    )

    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )


# -------------------------------------------------------------------------
# Front-end page routes
# -------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the existing calculator page."""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Serve the Module 13 login page."""

    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Serve the Module 13 registration page."""

    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )


# -------------------------------------------------------------------------
# Calculator API routes
# -------------------------------------------------------------------------

@app.post(
    "/add",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def add_route(operation: OperationRequest):
    """Add two numbers."""

    try:
        result = add(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as exc:
        logger.error("Add Operation Error: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(
    "/subtract",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def subtract_route(operation: OperationRequest):
    """Subtract two numbers."""

    try:
        result = subtract(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as exc:
        logger.error("Subtract Operation Error: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(
    "/multiply",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def multiply_route(operation: OperationRequest):
    """Multiply two numbers."""

    try:
        result = multiply(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as exc:
        logger.error("Multiply Operation Error: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(
    "/divide",
    response_model=OperationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def divide_route(operation: OperationRequest):
    """Divide two numbers."""

    try:
        result = divide(operation.a, operation.b)
        return OperationResponse(result=result)
    except ValueError as exc:
        logger.error("Divide Operation Error: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.error("Divide Operation Internal Error: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        ) from exc


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )