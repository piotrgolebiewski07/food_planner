import json
from pathlib import Path

from sqlalchemy import text

from food_planner_app import db
from food_planner_app.commands import db_manage_bp
from food_planner_app.models import Ingredient, Recipe


def load_json_data(file_name: str) -> list:
    json_path = Path(__file__).parent.parent / 'samples' / file_name
    with open(json_path) as file:
        data_json = json.load(file)
        return data_json


@db_manage_bp.cli.group()
def db_manage():
    """Database management commands"""
    pass


@db_manage.command()
def add_data():
    """Add sample data to database"""
    try:
        data_json = load_json_data('ingredients.json')
        for item in data_json:
            ingredient = Ingredient(**item)
            db.session.add(ingredient)

        data_json = load_json_data('recipes.json')
        for item in data_json:
            recipe = Recipe(**item)
            db.session.add(recipe)

        db.session.commit()
        print("Sample ingredients and recipes added successfully.")
    except Exception as exc:
        print('Unexpected error: {}'.format(exc))


@db_manage.command()
def remove_data():
    """Remove all data from the database"""
    try:
        db.session.execute(text('DELETE FROM recipes'))
        db.session.execute(text('ALTER TABLE recipes AUTO_INCREMENT = 1'))
        db.session.execute(text('DELETE FROM ingredients'))
        db.session.execute(text('ALTER TABLE ingredients AUTO_INCREMENT = 1'))
        db.session.commit()
        print('Data has been successfully remove from database')
    except Exception as exc:
        print('Unexpected error: {}'.format(exc))

