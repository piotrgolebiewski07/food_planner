import json
from pathlib import Path

from food_planner_app import create_app, db
from food_planner_app.models import Ingredient
from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = create_app()
print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])

with app.app_context():

    # ---- INGREDIENTS ----
    ingredients_path = DATA_DIR / "ingredients.json"
    if not ingredients_path.exists():
        raise FileNotFoundError(f"Missing file: {ingredients_path}")

    with open(ingredients_path, encoding="utf-8") as f:
        ingredients = json.load(f)

    print("ING FILE PATH:", ingredients_path)
    print("ING COUNT IN FILE:", len(ingredients))

    for item in ingredients:
        exists = Ingredient.query.filter_by(name=item["name"]).first()
        if not exists:
            db.session.add(
                Ingredient(
                    name=item["name"],
                    calories=item["calories"],
                    unit=item["unit"],
                )
            )

    db.session.commit()
    print("COUNT IN SESSION:", Ingredient.query.count())

print("Ingredients seeded.")