from datetime import datetime
from food_planner_app import db
from marshmallow import Schema, fields, validate, EXCLUDE
from decimal import Decimal


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    calories = db.Column(db.Numeric(6,2), nullable=False)  # kcal per 100g or 1 pc
    unit = db.Column(db.String(10), nullable=False, default="g")    # g/ml/pcs

    def __repr__(self):
        return f"<Ingredient {self.name}>"


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
    __tablename__ = ('users')
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), primary_key=True)
    amount = db.Column(db.Numeric(6,2), nullable=False)

    recipe = db.relationship("Recipe", back_populates="ingredients")
    ingredient = db.relationship("Ingredient")


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


ingredient_schema = IngredientSchema()
recipe_schema = RecipeSchema()

