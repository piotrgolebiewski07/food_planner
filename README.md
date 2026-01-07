# Food Planner API

Food Planner API is a lightweight REST backend built with **Flask** and **Flask-SQLAlchemy**.
It serves as a foundation for a future meal-planning system that will manage ingredients,
recipes, and meal schedules.

The current version focuses on core backend architecture and database integration and is
designed as a learning and portfolio-oriented backend project.

## Features

- Clean and simple REST API structure using Flask
- MySQL database integration with SQLAlchemy
- Database migrations with Alembic
- Environment-based configuration (`.env`)
- Modular application design
- CLI commands for database seeding
- Easily extendable for future modules (recipes, meals, planner)
- Flexible query filtering and sorting for API resources

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- MySQL
- Alembic

## Project Structure

```
food_planner_app/
├── __init__.py
├── models.py
├── ingredients.py
├── db_manage_commands.py
├── samples/
│   └── ingredients.json
migrations/
config.py
food_planner.py
```
## Setup (Local)

1. Create a virtual environment
2. Install dependencies
3. Create a .env file based on .env.example
4. Run database migrations
5. Start the application

## Current Scope

- Ingredient model
- Sample data loading via CLI commands
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
