from food_planner_app import db
from marshmallow import Schema, fields, validate


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    calories = db.Column(db.Float, nullable=False)  # kcal per 100g or 1 pc
    unit = db.Column(db.String(20), nullable=False, default="g")    # g/ml/pcs

    def __repr__(self):
        return f"<Ingredient {self.name}>"


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    servings = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<Recipe {self.name}>"

class IngredientSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    calories = fields.Float(required=True, validate=validate.Range(min=0))
    unit = fields.String(required=True, validate=validate.Length(max=10))


ingredient_schema = IngredientSchema()

