from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Swagger configuration
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Food Planner API",
            "description": "REST API for managing ingredients and recipes",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        }
    }
    Swagger(app, template=swagger_template)

    db.init_app(app)
    migrate.init_app(app, db)

    from food_planner_app.commands import db_manage_bp
    from food_planner_app.errors import errors_bp
    from food_planner_app.ingredients import ingredients_bp
    from food_planner_app.recipes import recipes_bp
    from food_planner_app.auth import auth_bp
    app.register_blueprint(db_manage_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(ingredients_bp, url_prefix='/api/v1')
    app.register_blueprint(recipes_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    return app

