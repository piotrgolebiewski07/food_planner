from flask import Blueprint

errors_bp = Blueprint('errors', __name__)

from food_planner_app.errors import errors

