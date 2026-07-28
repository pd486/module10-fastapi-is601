# Module 14 – FastAPI Frontend BREAD Application

## Overview

This project builds on the FastAPI Calculator from the previous modules by adding a frontend for managing calculations. Instead of only using the API through Swagger, users can now interact with the application through a web interface to create, view, edit, and delete calculations. The project uses FastAPI, SQLAlchemy, PostgreSQL, JWT authentication, JavaScript, Docker, and GitHub Actions.

## Features

- User registration
- User login using JWT authentication
- SQLAlchemy User model
- SQLAlchemy Calculation model
- Frontend interface for managing calculations
- Browse calculations
- Add new calculations
- Edit existing calculations
- Delete calculations
- Pydantic validation for requests and responses
- Factory Pattern for Add, Subtract, Multiply, and Divide operations
- Validation for supported calculation types
- Division-by-zero validation
- PostgreSQL database integration
- Unit, integration, and Playwright tests
- Interactive Swagger API documentation
- GitHub Actions CI/CD pipeline
- Docker Hub image deployment

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

Open the application:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

## Frontend

Module 14 adds a browser interface that allows users to manage calculations without using Swagger. After logging in, users can:

- View saved calculations
- Create new calculations
- Edit existing calculations
- Delete calculations

The frontend communicates with the FastAPI backend using JavaScript and authenticated API requests.

## Running Tests

Run the standard test suite:

```bash
pytest
```

Run all tests, including slow tests:

```bash
pytest --run-slow
```

The project includes:

- Unit tests
- Integration tests
- Authentication tests
- Database model tests
- API endpoint tests
- Playwright end-to-end tests

## API Endpoints

### Authentication

- POST `/users/register`
- POST `/users/login`

### Calculations

- GET `/calculations`
- GET `/calculations/{id}`
- POST `/calculations`
- PUT `/calculations/{id}`
- DELETE `/calculations/{id}`

## CI/CD

GitHub Actions automatically runs the project's tests whenever changes are pushed to GitHub. After the tests pass, the workflow performs a security scan, builds the Docker image, and pushes the latest image to Docker Hub.

## Docker Hub

Docker image:

https://hub.docker.com/r/pd486/module10-fastapi-is601

Pull the latest image:

```bash
docker pull pd486/module10-fastapi-is601:latest
```

## Reflection

See **Reflection.md** for a summary of the work completed in Module 14, the challenges encountered while building the frontend, and what I learned during the project.