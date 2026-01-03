from flask import jsonify, request
from webargs.flaskparser import use_args
from food_planner_app import app, db
from food_planner_app.models import Ingredient, IngredientSchema, ingredient_schema


@app.route('/api/v1/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    ingredient_schema = IngredientSchema(many=True)

    return jsonify({
        'success': True,
        'data': ingredient_schema.dump(ingredients),
        'number of records': len(ingredients)
    })


@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id: int):
    ingredient = Ingredient.query.get_or_404(ingredient_id, description=f'Ingredient with id {ingredient_id} not found')
    return jsonify({
        'success': True,
        'data': ingredient_schema.dump(ingredient)
    })


@app.route('/api/v1/ingredients', methods=['POST'])
@use_args(ingredient_schema)
def create_ingredient(args: dict):
    ingredient = Ingredient(**args)

    db.session.add(ingredient)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": ingredient_schema.dump(ingredient)
    }), 201


@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['PUT'])
@use_args(IngredientSchema(partial=True))
def update_ingredient(args: dict, ingredient_id: int):
    ingredient = Ingredient.query.get_or_404(ingredient_id, description=f'Ingredient with id {ingredient_id} not found')

    for key, value in args.items():
        setattr(ingredient, key, value)

    db.session.commit()

    return jsonify({
        'success': True,
        'data': ingredient_schema.dump(ingredient)
    })


@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id: int):
    ingredient = Ingredient.query.get_or_404(ingredient_id, description=f'Ingredient with id {ingredient_id} not found')

    db.session.delete(ingredient)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Ingredient with id {ingredient_id} has been deleted'
    })
