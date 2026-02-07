from food_planner_app import create_app, db
from food_planner_app.models import Ingredient

app = create_app()

with app.app_context():
    print("Flask context active.")
    print("Available objects:", db, Ingredient)

