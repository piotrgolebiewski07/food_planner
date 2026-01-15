from flask import Blueprint

recipes_bp = Blueprint('recipes', __name__)

from food_planner_app.recipes import recipes
