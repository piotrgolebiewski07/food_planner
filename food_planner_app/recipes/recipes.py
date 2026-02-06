from flask import request, abort
from flask import jsonify
from food_planner_app import db
from food_planner_app.recipes import recipes_bp
from food_planner_app.models import Recipe, RecipeIngredient, Ingredient
from food_planner_app.utils import validate_json_content_type, get_pagination, token_required
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError


@recipes_bp.route('/recipes', methods=['GET'])
def get_recipes():
    query = select(Recipe)
    items, pagination = get_pagination(query, 'recipes.get_recipes')

    data = []

    for recipe in items:
        data.append({
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "servings": recipe.servings,
            "ingredients": [
                {
                    "name": ri.ingredient.name,
                    "amount": float(ri.amount),
                    "unit": ri.ingredient.unit,
                    "calories": float(ri.ingredient.calories),
                }
                for ri in recipe.ingredients
            ]
        })

    return jsonify({
        "success": True,
        "data": data,
        "records_on_page": len(data),
        "pagination": pagination
    })


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)

    data = {
        "id": recipe.id,
        "name": recipe.name,
        "description": recipe.description,
        "servings": recipe.servings,
        "ingredients": [
            {
                "name": ri.ingredient.name,
                "amount": float(ri.amount),
                "unit": ri.ingredient.unit,
                "calories": float(ri.ingredient.calories),
            }
            for ri in recipe.ingredients
        ]
    }

    return jsonify({
        "success": True,
        "data": data
    })


@recipes_bp.route('/recipes/random', methods=['GET'])
def random_recipes():
    days = min(int(request.args.get("days", 7)), 14)

    recipes = (
        db.session.query(Recipe)
        .order_by(func.random())
        .limit(days)
        .all()
    )

    data = [
        {
            "id": r.id,
            "name": r.name,
            "servings": r.servings
        }
        for r in recipes
    ]

    return jsonify({
        "success": True,
        "days": days,
        "data": data
    })


@recipes_bp.route('/recipes', methods=['POST'])
@token_required
@validate_json_content_type
def create_recipe(user_id: int):
    data = request.get_json()

    recipe = Recipe(
        name=data["name"],
        description=data.get("description"),
        servings=data.get("servings", 1),
    )
    db.session.add(recipe)
    db.session.flush()

    for ing in data.get("ingredients", []):
        ingredient = Ingredient.query.filter_by(name=ing["name"]).first()
        if not ingredient:
            abort(400, description=f"Ingredient not found: {ing['name']}")

        db.session.add(
            RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                amount=ing["amount"],
            )
        )

    db.session.commit()

    return jsonify({
        "success": True,
        "data": {
            "id": recipe.id,
            "name": recipe.name
        }
    }), 201


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['PUT'])
@token_required
@validate_json_content_type
def update_recipe(user_id: int, recipe_id: int):
    data = request.get_json()

    recipe = Recipe.query.get_or_404(recipe_id)

    for field in ("name", "description", "servings"):
        if field in data:
            setattr(recipe, field, data[field])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "Recipe with this name already exists"
        }), 409

    return jsonify({
        "success": True,
        "data": {
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "servings": recipe.servings
        }
    }), 200


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@token_required
def delete_recipe(user_id: int, recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Recipe {recipe_id} deleted"
    }), 200

