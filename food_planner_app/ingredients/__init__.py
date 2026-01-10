from flask import Blueprint

ingredients_bp = Blueprint('ingredients', __name__)

from food_planner_app.ingredients import routes

