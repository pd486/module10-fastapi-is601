# Module 11 – FastAPI Calculation Model, Pydantic Validation, and CI/CD

## Overview
This project extends the FastAPI application by adding a SQLAlchemy `Calculation` model, Pydantic schemas for validation, and a Factory pattern to support multiple calculation types. The project maintains a complete CI/CD pipeline using GitHub Actions, PostgreSQL, and Docker Hub.

## Features
- SQLAlchemy `User` model with authentication
- SQLAlchemy `Calculation` model
- Pydantic `CalculationCreate` and `CalculationRead` schemas
- Factory Pattern for Add, Subtract, Multiply, and Divide operations
- Validation for supported calculation types and division by zero
- Unit, integration, and end-to-end tests
- PostgreSQL database support
- GitHub Actions CI/CD pipeline
- Docker Hub image deployment

## Running Tests Locally

### 1. Clone the repository and create a virtual environment

```bash
git clone https://github.com/pd486/module10-fastapi-is601.git
cd module10-fastapi-is601
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start PostgreSQL with Docker Compose

```bash
docker compose up -d
```

### 3. Run the complete test suite

```bash
pytest
```

Expected result:

- All tests pass
- High test coverage
- Unit, integration, and end-to-end tests execute successfully

### 4. Run the application

```bash
python main.py
```

The application will be available at:

```
http://127.0.0.1:8000
```

## CI/CD Pipeline

Every push to the `main` branch automatically performs the following:

1. Runs all unit, integration, and end-to-end tests.
2. Performs a security scan using Trivy.
3. Builds the Docker image.
4. Pushes the image to Docker Hub after all checks pass.

## Docker Hub

Docker image:

https://hub.docker.com/r/pd486/module10-fastapi-is601

Pull the latest image:

```bash
docker pull pd486/module10-fastapi-is601:latest
```

## Reflection

See `Reflection.md` for a summary of the work completed, challenges encountered, and lessons learned during Module 11.