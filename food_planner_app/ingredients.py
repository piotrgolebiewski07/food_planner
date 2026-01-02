from flask import jsonify, request
from food_planner_app import app, db
from food_planner_app.models import Ingredient


@app.route('/api/v1/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()

    data = [
        {
            "id": ingredient.id,
            "name": ingredient.name,
            "calories": ingredient.calories,
            "unit": ingredient.unit
        }
        for ingredient in ingredients
    ]

    return jsonify({
        'success': True,
        'count': len(data),
        'data': data
    })


@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id: int):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    data = {
            "id": ingredient.id,
            "name": ingredient.name,
            "calories": ingredient.calories,
            "unit": ingredient.unit
    }

    return jsonify({
        'success': True,
        'data': data
    })


@app.route('/api/v1/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            'success': False,
            'message': 'Request body must be json'
        }), 400

    ingredient = Ingredient(
        name=data.get("name"),
        calories=data.get("calories"),
        unit=data.get("unit","g")
    )

    db.session.add(ingredient)
    db.session.commit()

    response_data = {
        "id":  ingredient.id,
        "name":ingredient.name,
        "calories": ingredient.calories,
        "unit": ingredient.unit

    }

    return jsonify({
        "success": True,
        "data": response_data
    }), 201



@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id: int):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            'success': False,
            'message': 'Request body must be valid JSON'
        }), 400

    ingredient.name = data.get("name", ingredient.name)
    ingredient.calories = data.get("calories", ingredient.calories)
    ingredient.unit = data.get("unit", ingredient.unit)

    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'id': ingredient.id,
            'name': ingredient.name,
            'calories': ingredient.calories,
            'unit': ingredient.unit
        },
        'message': f'Ingredient with id {ingredient_id} has been updated'
    })


@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id: int):
    ingredient = Ingredient.query.get_or_404(ingredient_id)

    db.session.delete(ingredient)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Ingredient with id {ingredient_id} has been deleted'
    }), 200

