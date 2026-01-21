from flask import jsonify
from webargs.flaskparser import use_args
from food_planner_app import db
from food_planner_app.recipes import recipes_bp
from food_planner_app.models import Recipe, RecipeSchema, recipe_schema
from food_planner_app.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, get_pagination, token_required
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


@recipes_bp.route('/recipes', methods=['GET'])
def get_recipes():
    query = select(Recipe)
    schema_args = get_schema_args(Recipe)
    query = apply_order(Recipe, query)
    query = apply_filter(Recipe, query)
    items, pagination = get_pagination(query, 'recipes.get_recipes')

    recipes = RecipeSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': recipes,
        'records on page': len(recipes),
        'pagination': pagination
    })


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id, description=f'Recipe with id {recipe_id} not found')
    return jsonify({
        'success': True,
        'data': recipe_schema.dump(recipe)
    })


@recipes_bp.route('/recipes', methods=['POST'])
@token_required
@validate_json_content_type
@use_args(recipe_schema, error_status_code=400)
def create_recipe(user_id: str, args: dict):
    recipe = Recipe(**args)

    try:
        db.session.add(recipe)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "Recipe with this name already exists"
        }), 409

    return jsonify({
        "success": True,
        "data": recipe_schema.dump(recipe)
    }), 201


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(RecipeSchema(partial=True), error_status_code=400)
def update_recipe(user_id: str, args: dict, recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id, description=f'Recipe with id {recipe_id} not found')

    for key, values in args.items():
        setattr(recipe, key, values)

    db.session.commit()

    return jsonify({
        'success': True,
        'data': recipe_schema.dump(recipe)
    })


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@token_required
def delete_recipe(user_id: str, recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id, description=f'Recipe with id {recipe_id} not found')

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Recipe with id {recipe_id} has been deleted'
    })

