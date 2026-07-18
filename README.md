# Module 12 – FastAPI Authentication, BREAD API Endpoints, and CI/CD

## Overview

This project extends the FastAPI Calculator application by implementing user authentication and complete BREAD (Browse, Read, Edit, Add, Delete) functionality for calculation records. The application uses SQLAlchemy models, Pydantic schemas, JWT authentication, and PostgreSQL to provide a secure REST API. A complete CI/CD pipeline is maintained using GitHub Actions, Docker, and Docker Hub.

## Features

- User registration endpoint
- User login endpoint with JWT authentication
- SQLAlchemy `User` model
- SQLAlchemy `Calculation` model
- Full BREAD (Browse, Read, Edit, Add, Delete) API for calculations
- Pydantic validation for request and response models
- Factory Pattern for Add, Subtract, Multiply, and Divide operations
- Validation for supported calculation types and division by zero
- PostgreSQL database support
- Unit, integration, and end-to-end tests
- Interactive Swagger API documentation
- GitHub Actions CI/CD pipeline
- Docker Hub image deployment

---

## Running the Application

### 1. Clone the repository

```bash
git clone https://github.com/pd486/module10-fastapi-is601.git
cd module10-fastapi-is601
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL

```bash
docker compose up -d
```

### 5. Initialize the database

```bash
python -m app.database_init
```

### 6. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

Swagger/OpenAPI documentation:

```
http://127.0.0.1:8000/docs
```

---

## Running Tests Locally

Run the complete test suite:

```bash
pytest
```

Expected results:

- All unit tests pass
- All integration tests pass
- End-to-end tests execute successfully
- High test coverage

---

## API Endpoints

### Authentication

- `POST /users/register`
- `POST /users/login`

### Calculations

- `GET /calculations`
- `GET /calculations`
- `GET /calculations/{id}`
- `POST /calculations`
- `PUT /calculations/{id}`
- `DELETE /calculations/{id}`

---

## CI/CD Pipeline

Every push to the `main` branch automatically:

1. Runs all unit, integration, and end-to-end tests.
2. Performs a Trivy security scan.
3. Builds the Docker image.
4. Pushes the Docker image to Docker Hub after all checks pass.

---

## Docker Hub

Docker image:

https://hub.docker.com/r/pd486/module10-fastapi-is601

Pull the latest image:

```bash
docker pull pd486/module10-fastapi-is601:latest
```

---

## Reflection

See `Reflection.md` for a summary of the work completed, challenges encountered, and lessons learned while implementing user authentication, BREAD API endpoints, testing, and CI/CD during Module 12.