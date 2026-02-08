# Food Planner API

A backend-only REST API built with **Flask** and **SQLAlchemy** for managing **recipes** and **ingredients**.
The project focuses on clean API design, relational modeling (many-to-many with domain data), authentication, and integration testing.

## Why this project

This project was built to practice designing a non-trivial backend: protected endpoints, relational data modeling,
validation, and automated testing. It aims to be clear, maintainable, and easy to reason about.

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

Example endpoint:
```
GET /api/v1/recipes/random?days=7
```
## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- MySQL
- Alembic
- Pytest
  
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
README.md
```
## Testing

The project includes integration tests covering:
- Authentication flows
- Ingredients CRUD
- Recipes creation, Validation and authorization rules

Tests are written using Flask test client and focus on API behavior.

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
## Design Notes

- The project uses explicit domain modeling rather than generic schemas
- Recipes and ingredients are connected via a join table with domain data
- Serialization is handled manually where relationships are complex
- The code prioritizes readability and maintainability over abstraction

---

## Project Status

**Finished**

This project is considered complete and serves as a reference backend
application demonstrating Flask, relational modeling and API design.

## Query examples

The API supports basic filtering, sorting and field selection via query parameters.

Examples:
- `GET /api/v1/ingredients?calories[gte]=100`
- `GET /api/v1/ingredients?unit[ne]=g`
- `GET /api/v1/ingredients?fields=name,calories&sort=-calories`
