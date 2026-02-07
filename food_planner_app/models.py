from datetime import datetime, timedelta, timezone
from decimal import Decimal

import jwt
from flask import current_app
from marshmallow import EXCLUDE, Schema, fields, validate
from werkzeug.security import check_password_hash, generate_password_hash

from food_planner_app import db


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    calories = db.Column(db.Numeric(6,2), nullable=False)
    unit = db.Column(db.String(10), nullable=False, default="g")

    recipes = db.relationship(
        "RecipeIngredient",
        back_populates="ingredient",
        cascade="all, delete-orphan"
    )


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    description = db.Column(db.Text)
    servings = db.Column(db.Integer, nullable=False, default=1)

    ingredients = db.relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
        return f"<Recipe {self.name}>"


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @staticmethod
    def generate_hashed_password(password: str) -> str:
        return generate_password_hash(password)

    def is_password_valid(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def generate_jwt(self) -> bytes:
        payload = {
            'user_id': self.id,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=current_app.config.get('JWT_EXPIRED_MINUTES', 30))
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'))


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), primary_key=True)
    amount = db.Column(db.Numeric(6,2), nullable=False)

    recipe = db.relationship("Recipe", back_populates="ingredients")
    ingredient = db.relationship("Ingredient", back_populates="recipes")


class IngredientSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    calories = fields.Decimal(required=True, places=2, rounding=None, validate=validate.Range(min=Decimal("0.00")))
    unit = fields.String(required=True, validate=validate.OneOf(["g", "ml", "pcs"]))


class RecipeSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    description = fields.String(required=True, validate=validate.Length(min=2))
    servings = fields.Integer(required=True, validate=validate.Range(min=1))


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(max=255))
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    creation_date = fields.DateTime(dump_only=True)


class UserPasswordUpdateSchema(Schema):
    current_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    new_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))


class UserUpdateSchema(Schema):
    username = fields.String(required=False, validate=validate.Length(max=255))
    email = fields.Email(required=False)

    class Meta:
        unknown = EXCLUDE


ingredient_schema = IngredientSchema()
recipe_schema = RecipeSchema()
user_schema = UserSchema()
user_password_update_schema = UserPasswordUpdateSchema()
user_update_schema = UserUpdateSchema()

