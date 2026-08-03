# FastAPI Calculator Final Project

## Overview

This project is the completed FastAPI Calculator developed throughout the IS601 course. It provides a full-stack calculator application with user authentication, calculation management, and persistent data storage. The application uses FastAPI, SQLAlchemy, PostgreSQL, JWT authentication, JavaScript, Docker, and GitHub Actions to demonstrate modern web application development practices.

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
- Supported operations:
  - Add
  - Subtract
  - Multiply
  - Divide
  - Power
- Pydantic validation for requests and responses
- Factory Pattern for calculator operations
- Validation for supported calculation types
- Division-by-zero validation
- Power operation validation
- PostgreSQL database integration
- Unit, integration, and Playwright end-to-end tests
- Interactive Swagger API documentation
- GitHub Actions CI/CD pipeline
- Docker Hub image deployment

## Running the Application

### Clone the repository

```bash
git clone https://github.com/pd486/module10-fastapi-is601.git
cd module10-fastapi-is601
git checkout final-project
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

The web interface allows authenticated users to manage calculations without using Swagger. Users can:

- View saved calculations
- Create new calculations
- Edit existing calculations
- Delete calculations
- Perform Add, Subtract, Multiply, Divide, and Power operations

The frontend communicates with the FastAPI backend using JavaScript and authenticated API requests.

## Running Tests

Run the complete test suite:

```bash
pytest
```

Run unit tests:

```bash
pytest tests/unit -v
```

Run integration tests:

```bash
pytest tests/integration -v
```

Run Playwright end-to-end tests:

```bash
pytest tests/e2e -v
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

GitHub Actions automatically runs the project's test suite whenever changes are pushed to GitHub. After all tests pass, the workflow builds the Docker image and pushes the latest image to Docker Hub.

## Docker Hub

Docker image:

https://hub.docker.com/r/pd486/module10-fastapi-is601

Pull the latest image:

```bash
docker pull pd486/module10-fastapi-is601:latest
```

## GitHub Repository

Repository:

https://github.com/pd486/module10-fastapi-is601

Final Project Branch:

https://github.com/pd486/module10-fastapi-is601/tree/final-project

## Reflection

See **Reflection.md** for a summary of the development process, challenges encountered, and lessons learned while completing the FastAPI Calculator Final Project.