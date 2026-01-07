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

    @staticmethod  # metoda statyczna (chyba nie wymaga self)
    def get_schema_args(fields: str) -> dict:
        schema_args = {'many': True}
        if fields:
            schema_args['only'] = [field for field in fields.split(',') if field in Ingredient.__table__.columns.keys()]
        return schema_args

    @staticmethod
    def apply_order(query, sort_keys: str):
        if sort_keys:
            for key in sort_keys.split(','):
                desc = False
                if key.startswith('-'):
                    key = key[1:]
                    desc = True
                column_attr = getattr(Ingredient, key, None)
                if column_attr is not None:
                    query = query.order_by(column_attr.desc()) if desc else query.order_by(column_attr)
        return query

class IngredientSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    calories = fields.Float(required=True, validate=validate.Range(min=0))
    unit = fields.String(required=True, validate=validate.Length(max=10))


ingredient_schema = IngredientSchema()

