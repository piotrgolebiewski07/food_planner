# Food Planner API

A production-like backend REST API built with Flask, SQLAlchemy, and MySQL, fully containerized with Docker Compose.
The project demonstrates clean API architecture, relational modeling with domain logic, authentication, pagination, filtering, and integration testing.

## Why this project

This project was built to practice designing a non-trivial backend: protected endpoints, relational data modeling,
validation, and automated testing. It aims to be clear, maintainable, and easy to reason about.

## Architecture

The application runs as a multi-container setup:
```
Docker Network
├── foodplanner-app (Flask + Gunicorn)
└── foodplanner-db (MySQL 8)
      └── Persistent Docker Volume
```
The database is initialized using Alembic migrations and seeded for development.

- Services communicate over internal Docker network
- Database state is persisted using Docker volumes
- Application runs behind Gunicorn (WSGI production server)

## Running with Docker

```
docker compose up --build
```
API will be available at:
```
http://localhost:5000/api/v1/ingredients
```

## Tech Stack
### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Alembic (database migrations)
- Gunicorn (production WSGI server)
### Database
- MySQL 8
### Testing
- Pytest
- Flask test client
### Infrastructure
- Docker
- Docker Compose 

## API Design & Security

- Consistent URL versioning (`/api/v1`)
- Structured JSON responses (`success`, `data`, `pagination`)
- Explicit error handling and validation responses
- Query-based filtering and field selection
- JWT-based authentication
- Protected endpoints with role-aware access
- Input validation
- Environment-based configuration

## Example endpoint:
```
GET /api/v1/recipes/random?days=7
```

## Query Examples
```
GET /api/v1/ingredients?calories[gte]=100
GET /api/v1/ingredients?fields=name,calories
GET /api/v1/ingredients?sort=-calories
```

## Example Response
```
{
  "success": true,
  "data": [...],
  "pagination": {
      "current_page": "...",
      "total_pages": 5
  }
}
```

## Key Highlights

- REST API with full CRUD functionality
- Many-to-many relationship with additional domain data (`amount` in join table)
- JWT authentication and protected endpoints
- Pagination, filtering, sorting, and field selection
- Integration tests with Pytest
- Alembic database migrations

## Features

### Authentication
- User registration and login
- JWT-based authentication
- Protected endpoints
- Validation and error handling

### Ingredients (CRUD)
- List ingredients (pagination, filters, sorting)
- Retrieve a single ingredient
- Create, update and delete ingredients
- Duplicate protection and validation

### Recipes (CRUD)
- Many-to-many relationship with ingredients
- Additional domain field (`amount`) stored in join table
- Create, read, update and delete recipes
- Random recipe selection endpoint

## Testing

The project includes integration tests covering:
- Authentication flows
- Authorization rules
- CRUD operations
- Validation logic
- Domain constraints

Tests are written using Pytest and executed against the application context.

## Project Structure

```
food_planner_app/
├── auth/
├── ingredients/
├── recipes/
├── models.py
├── utils.py
tests/
├── test_auth.py
├── test_ingredients.py
├── test_recipes.py
├── conftest.py
migrations/
config.py
seed.py
Dockerfile
docker-compose.yml
README.md
```

## Design Decisions

- App Factory pattern for scalability
- Explicit domain modeling instead of generic serializers
- Production-like containerized environment
- Separation of concerns by feature modules
- Integration-first testing approach

## Setup (Local)

1. Create a virtual environment
2. Install dependencies
3. Create a `.env` file based on `.env.example`
4. Run database migrations
5. Start the application
```
pip install -r requirements.txt
flask db upgrade
flask run
```

## Environment Variables
The application uses environment-based configuration.
Required variables are documented in `.env.example`.

## Project Status

**Finished**

Production-like backend API for portfolio and technical demonstration purposes.
