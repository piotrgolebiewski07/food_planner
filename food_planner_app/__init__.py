from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from food_planner_app.commands import db_manage_bp
    from food_planner_app.errors import errors_bp
    from food_planner_app.ingredients import ingredients_bp
    app.register_blueprint(db_manage_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(ingredients_bp, url_prefix='/api/v1')

    return app


