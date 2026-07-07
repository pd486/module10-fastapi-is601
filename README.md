# Module 10 – FastAPI Secure User Model, Testing, and CI/CD

## Overview
This project enhances a FastAPI application with a secure SQLAlchemy `User` model,
Pydantic schemas for validation, password hashing, and a full CI/CD pipeline using
GitHub Actions and Docker Hub.

## Features
- SQLAlchemy `User` model with unique `username`/`email` constraints and `created_at` timestamp
- Pydantic `UserCreate` / `UserRead` schemas
- Secure password hashing and verification (passlib)
- Unit and integration tests (PostgreSQL-backed)
- GitHub Actions CI/CD pipeline: test → security scan → Docker Hub deploy

## Running Tests Locally

### 1. Clone the repo and set up a virtual environment
```bash
git clone https://github.com/pd486/module10-fastapi-is601.git
cd module10-fastapi-is601
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start PostgreSQL via Docker Compose
```bash
docker compose up -d
```

### 3. Run the test suite
```bash
pytest
```

Expected result: all tests passing with high coverage.

### 4. Run the app locally
```bash
python main.py
```
The app will be available at `http://127.0.0.1:8000`.

## CI/CD Pipeline
On every push to `main`, GitHub Actions runs:
1. **test** – runs unit, integration, and e2e tests against a PostgreSQL service container
2. **security** – builds the Docker image and scans it with Trivy
3. **deploy** – pushes the built image to Docker Hub (only on `main`)

## Docker Hub

The built image is published here:
👉 **https://hub.docker.com/r/pd486/module10-fastapi-is601**

Pull it directly:
```bash
docker pull pd486/module10-fastapi-is601:latest
```

## Screenshots
- `screenshots/github-actions-success.png` – successful CI/CD run
- `screenshots/docker-hub-deployment.png` – Docker Hub repo with published tags

## Reflection
See `REFLECTION.md` for a summary of challenges and lessons learned during this module.
