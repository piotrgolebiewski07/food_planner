from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# import after Blueprint creation to avoid circular imports
from food_planner_app.auth import auth  # noqa: E402

