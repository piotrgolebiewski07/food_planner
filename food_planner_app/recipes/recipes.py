from flask import abort, jsonify, request
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from food_planner_app import db
from food_planner_app.models import Ingredient, Recipe, RecipeIngredient
from food_planner_app.recipes import recipes_bp
from food_planner_app.utils import (
    get_pagination,
    token_required,
    validate_json_content_type,
)


@recipes_bp.route('/recipes', methods=['GET'])
def get_recipes():
    """
    Get all recipes
    ---
    tags:
      - Recipes
    produces:
      - application/json
    parameters:
      - in: query
        name: page
        type: integer
        required: false
      - in: query
        name: per_page
        type: integer
        required: false
    responses:
      200:
        description: List of recipes
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  description:
                    type: string
                  servings:
                    type: integer
                  ingredients:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                          type: string
                        amount:
                          type: number
                        unit:
                          type: string
                        calories:
                          type: number
            records_on_page:
              type: integer
            pagination:
              type: object
    """
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
    """
    Get recipe by ID
    ---
    tags:
      - Recipes
    produces:
      - application/json
    parameters:
      - in: path
        name: recipe_id
        type: integer
        required: true
    responses:
      200:
        description: Recipe found
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
      404:
        description: Recipe not found
    """
    recipe = db.session.get(Recipe, recipe_id)

    if recipe is None:
        abort(404)

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
    """
    Get random recipes
    ---
    tags:
      - Recipes
    produces:
      - application/json
    parameters:
      - in: query
        name: days
        type: integer
        required: false
        description: Number of days (max 14)
    responses:
      200:
        description: Random recipes
        schema:
          type: object
          properties:
            success:
              type: boolean
            days:
              type: integer
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  servings:
                    type: integer
    """
    try:
        days = int(request.args.get("days", 7))
    except ValueError:
        abort(400, description="Invalid days parameter")

    days = min(days, 14)

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
def create_recipe(_user_id: int):
    """
    Create new recipe
    ---
    tags:
      - Recipes
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - instructions
            - ingredients
          properties:
            name:
              type: string
              example: Pancakes
            instructions:
              type: string
              example: Mix ingredients and fry
            servings:
              type: integer
              example: 2
            ingredients:
              type: array
              items:
                type: object
                required:
                  - name
                  - amount
                properties:
                  name:
                    type: string
                    example: Milk
                  amount:
                    type: number
                    example: 200
    responses:
      201:
        description: Recipe created
      400:
        description: Validation error
    """
    data = request.get_json()

    if not data:
        abort(400, description="Invalid JSON body")

    required_fields = ["name", "instructions", "ingredients"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({
            "success": False,
            "message": {f: ["Missing data for required field."] for f in missing}
        }), 400

    recipe = Recipe(
        name=data["name"],
        description=data.get("instructions"),
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
def update_recipe(_user_id: int, recipe_id: int):
    """
    Update recipe
    ---
    tags:
      - Recipes
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: recipe_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            servings:
              type: integer
    responses:
      200:
        description: Recipe updated
      404:
        description: Recipe not found
      409:
        description: Duplicate recipe name
    """
    data = request.get_json()

    if not data:
        abort(400, description="Invalid JSON body")

    recipe = db.session.get(Recipe, recipe_id)

    if recipe is None:
        abort(404)

    for field in ("name", "description", "servings"):
        if field in data:
            setattr(recipe, field, data[field])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Recipe with this name already exists")

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
def delete_recipe(_user_id: int, recipe_id: int):
    """
    Delete recipe
    ---
    tags:
      - Recipes
    produces:
      - application/json
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: recipe_id
        type: integer
        required: true
    responses:
      200:
        description: Recipe deleted
      404:
        description: Recipe not found
    """
    recipe = db.session.get(Recipe, recipe_id)

    if recipe is None:
        abort(404)

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Recipe {recipe_id} deleted"
    }), 200

