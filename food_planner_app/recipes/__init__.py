from flask import Blueprint

recipes_bp = Blueprint('recipes', __name__)

# import after Blueprint creation to avoid circular imports
from food_planner_app.recipes import recipes  # noqa: E402

