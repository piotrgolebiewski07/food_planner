from flask import jsonify
from food_planner_app import app


@app.route('/api/v1/ingredients', methods=['GET'])
def get_ingredients():
    return jsonify({
        'success': True,
        'data': 'Get all ingredients'
    })


@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id: int):
    return jsonify({
        'success': True,
        'data': f'Get single ingredient with id {ingredient_id}'
    })


@app.route('/api/v1/ingredients', methods=['POST'])
def create_ingredient():
    return jsonify({
        'success': True,
        'data': 'New ingredient has been created'
    }), 201


@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id: int):
    return jsonify({
        'success': True,
        'data': f'Ingredient with id {ingredient_id} has been updated'
    })


@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id: int):
    return jsonify({
        'success': True,
        'data': f'Ingredient with id {ingredient_id} has been deleted'
    })

