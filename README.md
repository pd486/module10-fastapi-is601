# Module 12 & 13 – FastAPI Authentication, Calculations, and CI/CD

## Overview

This project extends the FastAPI Calculator application by implementing user authentication, calculation management, and automated testing. The application uses FastAPI, SQLAlchemy, PostgreSQL, JWT authentication, Docker, and GitHub Actions to provide a secure REST API with continuous integration and deployment.

Module 12 focused on implementing user authentication, API endpoints, and CI/CD. Module 13 expanded the project by refining calculation validation, increasing test coverage, and improving the overall project organization.

---

## Features

- User registration
- User login using JWT authentication
- SQLAlchemy User model
- SQLAlchemy Calculation model
- Calculation BREAD API endpoints
- Pydantic schemas for request and response validation
- Factory Pattern for Add, Subtract, Multiply, and Divide operations
- Validation for supported calculation types
- Division-by-zero validation
- PostgreSQL database integration
- Unit, integration, and Playwright end-to-end tests
- Interactive Swagger API documentation
- GitHub Actions CI/CD pipeline
- Docker Hub image deployment

---

## Running the Application

### Clone the repository

```bash
git clone https://github.com/pd486/module10-fastapi-is601.git
cd module10-fastapi-is601
```

### Create and activate a virtual environment

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

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start PostgreSQL

```bash
docker compose up -d
```

### Initialize the database

```bash
python -m app.database_init
```

### Start the application

```bash
uvicorn app.main:app --reload
```

The application is available at:

```
http://127.0.0.1:8000
```

Swagger/OpenAPI documentation:

```
http://127.0.0.1:8000/docs
```

---

## Running Tests

Run the standard test suite:

```bash
pytest
```

Run the complete test suite, including slow tests:

```bash
pytest --run-slow
```

Current test results:

- 94 tests passed
- 1 slow test skipped (default)
- 95 tests passed when running with `--run-slow`

Testing includes:

- Unit tests
- Integration tests
- Authentication tests
- Database model tests
- API endpoint tests
- Playwright end-to-end tests

---

## API Endpoints

### Authentication

- `POST /users/register`
- `POST /users/login`

### Calculations

- `GET /calculations`
- `GET /calculations/{id}`
- `POST /calculations`
- `PUT /calculations/{id}`
- `DELETE /calculations/{id}`

---

## CI/CD

Each push to the repository triggers a GitHub Actions workflow that:

1. Runs unit, integration, and Playwright tests.
2. Performs a Trivy security scan.
3. Builds the Docker image.
4. Pushes the Docker image to Docker Hub after all checks pass.

The workflow completed successfully with all automated tests passing before deployment.

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

See **Reflection.md** for a summary of the work completed, challenges encountered, testing experience, and lessons learned while developing Modules 12 and 13.
