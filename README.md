# Food Planner API

Food Planner API is a RESTful backend built with **Flask** and **Flask-SQLAlchemy**, focused on
API design, automated testing, and clean backend architecture.

## Key Highlights

- Fully tested REST API (pytest, integration tests)
- Clear separation of concerns (auth, ingredients)
- CRUD operations with validation and error handling
- Token-based authentication (JWT)
- Pagination, filtering, sorting, and field selection
- Clean Git workflow (feature branches, atomic commits)

## Features

- Clean and simple REST API structure using Flask
- MySQL database integration with SQLAlchemy
- Database migrations with Alembic
- Environment-based configuration (`.env`)
- Modular application design
- CLI commands for database seeding
- Easily extendable for future modules (recipes, meals, planner)
- Flexible query filtering and sorting for API resources

### Authentication
- User registration
- Login with JWT
- Auth-protected endpoints
- Validation and error handling

### Ingredients (CRUD)
- GET ingredients list (pagination, filters, sorting)
- GET single ingredient
- CREATE ingredient (auth required)
- DELETE ingredient (auth required)
- Validation and duplicate protection

All endpoints are covered by **integration tests**.

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- MySQL
- Alembic
- pytest
  
## Project Structure

```
food_planner_app/
├── auth/
├── ingredients/
├── models.py
├── utils.py
├── commands/
tests/
├── test_auth.py
├── test_ingredients.py
├── conftest.py
config.py
```
## Testing

The project includes a comprehensive pytest suite:
- Authentication tests
- Ingredients CRUD tests
- Validation and error scenarios
- Authorization checks
  
Tests are written as integration tests using Flask test client,
focusing on API behavior rather than implementation details.

## Setup (Local)

1. Create a virtual environment
2. Install dependencies
3. Create a .env file based on .env.example
4. Run database migrations
5. Start the application

## Current Scope

- Authentication with JWT
- Ingredients CRUD with validation and pagination
- Integration tests covering API behavior
- Database schema managed with migrations

## Future Plans

- Recipes and meals domain models
- Meal planning and scheduling
- Calorie calculations and data analysis (Pandas / ML)
- Recommendation logic based on user data

## Notes

This project is intentionally kept lightweight and readable.
It is intended as a foundation for further backend and data-oriented development.

## Query examples

The API supports basic filtering, sorting and field selection via query parameters.

Examples:

- GET /api/v1/ingredients?calories[gte]=100
- GET /api/v1/ingredients?unit[ne]=g
- GET /api/v1/ingredients?fields=name,calories&sort=-calories

## Quick Start

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate   # Windows
pip install -r requirements.txt
flask db upgrade
flask run
