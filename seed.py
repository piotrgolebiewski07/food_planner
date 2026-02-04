import json
from pathlib import Path

from food_planner_app import create_app, db
from food_planner_app.models import Ingredient, Recipe, RecipeIngredient
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

    # ---- RECIPES ----
    recipes_path = DATA_DIR / "recipes.json"
    if not recipes_path.exists():
        raise FileNotFoundError(f"Missing file: {recipes_path}")

    with open(recipes_path, encoding="utf-8") as f:
        recipes = json.load(f)

    print("RECIPES FILE PATH:", recipes_path)
    print("RECIPES COUNT IN FILE:", len(recipes))

    for item in recipes:
        # pomiń, jeśli już istnieje
        if Recipe.query.filter_by(name=item["name"]).first():
            continue

        recipe = Recipe(
            name=item["name"],
            description=item.get("description"),
            servings=item.get("servings", 1),
        )
        db.session.add(recipe)
        db.session.flush()  # mamy recipe.id

        for ing in item.get("ingredients", []):
            ingredient = Ingredient.query.filter_by(name=ing["name"]).first()
            if not ingredient:
                raise ValueError(f"Ingredient not found: {ing['name']}")

            db.session.add(
                RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    amount=ing["amount"],
                )
            )

    db.session.commit()
    print("Recipes seeded.")

print("Ingredients seeded.")