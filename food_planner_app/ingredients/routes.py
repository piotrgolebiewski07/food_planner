from flask import abort, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import use_args

from food_planner_app import db
from food_planner_app.ingredients import ingredients_bp
from food_planner_app.models import Ingredient, IngredientSchema, ingredient_schema
from food_planner_app.utils import (
    apply_filter,
    apply_order,
    get_pagination,
    get_schema_args,
    token_required,
    validate_json_content_type,
)


@ingredients_bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    """
    Get all ingredients
    ---
    tags:
      - Ingredients
    produces:
      - application/json
    security:
      - BearerAuth: []
    parameters:
      - in: query
        name: page
        type: integer
        required: false
        description: Page number
      - in: query
        name: per_page
        type: integer
        required: false
        description: Items per page
    responses:
      200:
        description: List of ingredients
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
            records_on_page:
              type: integer
            pagination:
              type: object
    """
    query = select(Ingredient)
    schema_args = get_schema_args(Ingredient)
    query = apply_order(Ingredient, query)
    query = apply_filter(Ingredient, query)
    items, pagination = get_pagination(query, 'ingredients.get_ingredients')
    ingredients = IngredientSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': ingredients,
        'records_on_page': len(ingredients),
        'pagination': pagination
    })


@ingredients_bp.route('/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id: int):
    """
    Get ingredient by ID
    ---
    tags:
      - Ingredients
    produces:
      - application/json
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: ingredient_id
        type: integer
        required: true
    responses:
      200:
        description: Ingredient found
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
      404:
        description: Ingredient not found
    """
    ingredient = db.session.get(Ingredient, ingredient_id)
    if not ingredient:
        abort(404, description=f'Ingredient with id {ingredient_id} not found')
    return jsonify({
        'success': True,
        'data': ingredient_schema.dump(ingredient)
    })


@ingredients_bp.route('/ingredients', methods=['POST'])
@token_required
@validate_json_content_type
@use_args(ingredient_schema, error_status_code=400)
def create_ingredient(user_id: int, args: dict):
    """
    Create new ingredient
    ---
    tags:
      - Ingredients
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
            - unit
            - calories
          properties:
            name:
              type: string
              example: Tomato
            unit:
              type: string
              example: g
            calories:
              type: number
              example: 18
    responses:
      201:
        description: Ingredient created
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
      400:
        description: Validation error
      409:
        description: Ingredient already exists
    """
    ingredient = Ingredient(**args)

    try:
        db.session.add(ingredient)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Ingredient with this name already exists")

    return jsonify({
        "success": True,
        "data": ingredient_schema.dump(ingredient)
    }), 201


@ingredients_bp.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(IngredientSchema(partial=True),  error_status_code=400)
def update_ingredient(user_id: int, args: dict, ingredient_id: int):
    """
    Update ingredient
    ---
    tags:
      - Ingredients
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: ingredient_id
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
              example: Updated Tomato
    responses:
      200:
        description: Ingredient updated
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
      400:
        description: Validation error
      404:
        description: Ingredient not found
    """
    ingredient = db.session.get(Ingredient, ingredient_id)
    if not ingredient:
        abort(404, description=f'Ingredient with id {ingredient_id} not found')

    for key, values in args.items():
        setattr(ingredient, key, values)

    db.session.commit()

    return jsonify({
        'success': True,
        'data': ingredient_schema.dump(ingredient)
    })


@ingredients_bp.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
@token_required
def delete_ingredient(user_id: int, ingredient_id: int):
    """
    Delete ingredient
    ---
    tags:
      - Ingredients
    produces:
      - application/json
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: ingredient_id
        type: integer
        required: true
    responses:
      200:
        description: Ingredient deleted
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
      404:
        description: Ingredient not found
    """
    ingredient = db.session.get(Ingredient, ingredient_id)
    if not ingredient:
        abort(404, description=f'Ingredient with id {ingredient_id} not found')

    db.session.delete(ingredient)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Ingredient with id {ingredient_id} has been deleted'
    })

