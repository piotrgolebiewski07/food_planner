from flask import Blueprint

errors_bp = Blueprint('errors', __name__)

# import after Blueprint creation to avoid circular imports
from food_planner_app.errors import errors  # noqa: E402

