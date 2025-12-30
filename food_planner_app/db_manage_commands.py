import json
from pathlib import Path
from food_planner_app import app, db
from food_planner_app.models import Ingredient
from sqlalchemy import text

@app.cli.group()
def db_manage():
    """Database management commands"""
    pass


@db_manage.command()
def add_data():
    """Add sample data to database"""
    try:
        ingredients_path = Path(__file__).parent / 'samples' / 'ingredients.json'
        with open(ingredients_path) as file:
            data_json = json.load(file)
        for item in data_json:
            ingredient = Ingredient(**item)  #**wypakowywanie
            db.session.add(ingredient)
        db.session.commit()
    except Exception as exc:
        print('Unexpected error: {}'.format(exc))


@db_manage.command()
def remove_data():
    """Remove all data from the database"""
    try:
        db.session.execute(text('TRUNCATE TABLE ingredients'))
        db.session.commit()
        print('Data has benn successfully remove from database')
    except Exception as exc:
        print('Unexpected error: {}'.format(exc))

