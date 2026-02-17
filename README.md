# Food Planner API
Production-style REST API built with Flask, SQLAlchemy, and MySQL.  
Fully containerized with Docker Compose.

This project demonstrates backend development skills including API design, relational modeling, authentication, validation, and automated testing.

## Quick Start (Docker)
```
docker compose up --build
```
Swagger UI:
```
http://localhost:5000/apidocs
```

## Tech Stack
- Python
- Flask
- SQLAlchemy + Alembic
- MySQL 8
- Gunicorn
- Docker & Docker Compose 
- Pytest
- Swagger (Flasgger)

## API Features
- JWT authentication
- Protected endpoints
- Structured JSON responses
- Pagination, filtering, sorting, field selection
- Many-to-many relationship (Recipe ↔ Ingredient)
- Domain data stored in join table (amount)
- Automatic DB migrations
- Seed data on startup

## Example Endpoint
```
GET /api/v1/recipes/random?days=7
```

## Tests
Integration tests written with Pytest covering:
- Authentication 
- Authorization
- CRUD operations
- Validation logic
- Domain constraints

Run tests
```
python -m pytest
```

## Project Structure
```
food_planner_app/
├── auth/
├── ingredients/
├── recipes/
├── models.py
├── utils.py
tests/
migrations/
Dockerfile
docker-compose.yml
README.md
```

## Status
Finished – portfolio backend project.

