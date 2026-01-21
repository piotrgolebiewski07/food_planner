import json
from pathlib import Path

from food_planner_app import create_app, db
from food_planner_app.models import Ingredient, Recipe

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = create_app()

with app.app_context():
    # ---- INGREDIENTS ----
    ingredients_path = DATA_DIR / "ingredients.json"
    if not ingredients_path.exists():
        raise FileNotFoundError(f"Missing file: {ingredients_path}")

    with open(ingredients_path, encoding="utf-8") as f:
        ingredients = json.load(f)

    for item in ingredients:
        exists = Ingredient.query.filter_by(name=item["name"]).first()
        if not exists:
            db.session.add(Ingredient(**item))

    # ---- RECIPES ----
    recipes_path = DATA_DIR / "recipes.json"
    if not recipes_path.exists():
        raise FileNotFoundError(f"Missing file: {recipes_path}")

    with open(recipes_path, encoding="utf-8") as f:
        recipes = json.load(f)

    for item in recipes:
        exists = Recipe.query.filter_by(name=item["name"]).first()
        if not exists:
            db.session.add(Recipe(**item))

    db.session.commit()

print("Seed completed.")