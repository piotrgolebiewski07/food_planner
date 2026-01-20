from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from food_planner_app.auth import auth

