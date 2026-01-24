import jwt
import re
from flask import url_for, current_app, abort
from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from functools import wraps
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import BinaryExpression
from flask import request, url_for
from food_planner_app import Config, db

COMPARISON_OPERATORS_RE = re.compile(r'(.*)\[(eq|gte|gt|lte|lt|ne)\]')


def validate_json_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = request.get_json(silent=True)
        except BadRequest:
            abort(400, description="Invalid JSON body")

        if data is None:
            abort(415,description='Content type must be application/json')

        return func(*args, **kwargs)
    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        token = None
        auth = request.headers.get('Authorization')
        if auth and auth.startswith('Bearer '):
            token = auth.split(' ')[1]
        else:
            abort(401, description='Missing or invalid Authorization header')

        try:
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET_KEY'),
                algorithms=['HS256']
                )
        except jwt.ExpiredSignatureError:
            abort(401, description='Expired token. Please login to get new token')
        except jwt.InvalidTokenError:
            abort(401, description='Invalid token. Please login or register')
        else:
            return func(payload['user_id'], *args, **kwargs)
    return wrapper


def get_schema_args(model) -> dict:
    """
    Reads ?fields=... from URL and builds arguments for Marshmallow schema.
    Allows selecting only specific columns of a model.
    """
    schema_args = {'many': True}
    fields = request.args.get('fields')
    if fields:
        schema_args['only'] = [field for field in fields.split(',') if field in model.__table__.columns]
    return schema_args


def apply_order(model, query):
    sort_keys = request.args.get('sort')
    if sort_keys:
        for key in sort_keys.split(','):
            desc = False
            if key.startswith('-'):
                key = key[1:]
                desc = True
            column_attr = getattr(model, key, None)
            if column_attr is not None:
                query = query.order_by(column_attr.desc()) if desc else query.order_by(column_attr)
    return query


def _get_filter_argument(column_name: InstrumentedAttribute, value: str, operator: str) -> BinaryExpression: #funkcja prywatna
    operator_mapping = {
        'eq': column_name == value,
        'gte': column_name >= value,
        'gt': column_name > value,
        'lte': column_name <= value,
        'lt': column_name < value,
        'ne': column_name != value
    }
    return operator_mapping[operator]


def apply_filter(model, query):
    for param, value in request.args.items():
        if param not in {'fields', 'sort', 'page', 'limit'}:
            operator = 'eq'
            match = COMPARISON_OPERATORS_RE.match(param)
            if match is not None:
                param, operator = match.groups()
            column_attr = getattr(model, param, None)
            if column_attr is not None:
                filter_argument = _get_filter_argument(column_attr, value, operator)
                query = query.filter(filter_argument)
    return query


def get_pagination(stmt, func_name: str):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', current_app.config.get('PER_PAGE', 5), type=int)

    params = {key: value for key, value in request.args.items() if key not in {'page', 'limit'}}

    pagination_obj = db.paginate(
        stmt,
        page=page,
        per_page=per_page,
        error_out=False
    )

    pagination = {
        'total_pages': pagination_obj.pages,
        'total_records': pagination_obj.total,
        'current_page': url_for(func_name, page=page, **params)
    }

    if pagination_obj.has_next:
        pagination['next_page'] = url_for(func_name, page=page + 1, **params)

    if pagination_obj.has_prev:
        pagination['previous_page'] = url_for(func_name, page=page - 1, **params)

    return pagination_obj.items, pagination

