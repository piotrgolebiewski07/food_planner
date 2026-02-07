from flask import Blueprint

ingredients_bp = Blueprint('ingredients', __name__)

# import after Blueprint creation to avoid circular imports
from food_planner_app.ingredients import routes  # noqa: E402

