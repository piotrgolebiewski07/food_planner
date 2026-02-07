from flask import Blueprint

db_manage_bp = Blueprint('db_manage_cmd', __name__, cli_group=None)

# import after Blueprint creation to avoid circular imports
from food_planner_app.commands import db_manage_commands  # noqa: E402

