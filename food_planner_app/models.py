import re
from food_planner_app import db
from marshmallow import Schema, fields, validate
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import BinaryExpression
from flask import request, url_for
from food_planner_app import Config


COMPARISON_OPERATORS_RE = re.compile(r'(.*)\[(gte|gt|lte|lt|ne)\]')


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    calories = db.Column(db.Float, nullable=False)  # kcal per 100g or 1 pc
    unit = db.Column(db.String(20), nullable=False, default="g")    # g/ml/pcs

    def __repr__(self):
        return f"<Ingredient {self.name}>"

    @staticmethod
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

    @staticmethod
    def get_filter_argument(column_name: InstrumentedAttribute, value: str, operator: str) -> BinaryExpression:
        operator_mapping = {
            '==': column_name == value,
            'gte': column_name >= value,
            'gt': column_name > value,
            'lte': column_name <= value,
            'lt': column_name < value,
            'ne': column_name != value
        }
        return operator_mapping[operator]

    @staticmethod
    def apply_filter(query):
        for param, value in request.args.items():
            if param not in {'fields', 'sort', 'page', 'limit'}:
                operator = '=='
                match = COMPARISON_OPERATORS_RE.match(param)
                if match is not None:
                    param, operator = match.groups()
                column_attr = getattr(Ingredient, param, None)
                if column_attr is not None:
                    filter_argument = Ingredient.get_filter_argument(column_attr, value, operator)
                    query = query.filter(filter_argument)
        return query

    @staticmethod
    def get_pagination(stmt):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', Config.PER_PAGE, type=int)

        params = {key: value for key, value in request.args.items() if key != 'page'}

        pagination_obj = db.paginate(
            stmt,
            page=page,
            per_page=per_page,
            error_out=False
        )

        pagination = {
            'total_pages': pagination_obj.pages,
            'total_records': pagination_obj.total,
            'current_page': url_for('get_ingredients', page=page, **params)
        }

        if pagination_obj.has_next:
            pagination['next_page'] = url_for('get_ingredients', page=page + 1, **params)

        if pagination_obj.has_prev:
            pagination['previous_page'] = url_for('get_ingredients', page=page - 1, **params)

        return pagination_obj.items, pagination


class IngredientSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    calories = fields.Float(required=True, validate=validate.Range(min=0))
    unit = fields.String(required=True, validate=validate.Length(max=10))


ingredient_schema = IngredientSchema()

