from flask import abort, jsonify
from webargs.flaskparser import use_args
from food_planner_app import db
from food_planner_app.auth import auth_bp
from food_planner_app.models import User, user_schema, UserSchema, user_password_update_schema, user_update_schema
from food_planner_app.utils import validate_json_content_type, token_required
from sqlalchemy.exc import IntegrityError


@auth_bp.route('/register', methods=['POST'])
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    if User.query.filter(User.username == args['username']).first():
        abort(409, description=f"User with username {args['username']} already exists")
    if User.query.filter(User.email == args['email']).first():
        abort(409, description=f"User with email {args['email']} already exists")

    args['password'] = User.generate_hashed_password(args['password'])
    user = User(**args)

    db.session.add(user)
    db.session.commit()

    token = user.generate_jwt()

    return jsonify({
        'success': True,
        'token': token
    }), 201


@auth_bp.route('/login', methods=['POST'])
@validate_json_content_type
@use_args(UserSchema(only=['username', 'password']), error_status_code=400)
def login(args: dict):
    user = User.query.filter(User.username == args['username']).first()
    if not user or not user.is_password_valid(args['password']):
        abort(401, description="Invalid credentials")

    token = user.generate_jwt()

    return jsonify({
        'success': True,
        'token': token
    })


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user_id: int):
    user = db.session.get(User, user_id)
    if not user:
        abort(404, description=f'User with id {user_id} not found')

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })


@auth_bp.route('/update/password/', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(user_password_update_schema, error_status_code=400)
def update_user_password(user_id: int, args: dict):
    user = db.Session.get(User, user_id)
    if not user:
        abort(404, description=f'User with id {user_id} not found')

    if not user.is_password_valid(args['current_password']):
        abort(401, description="Invalid password")

    user.password = user.generate_hashed_password(args['new_password'])
    db.session.commit()

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })


@auth_bp.route('/update/data/', methods=['PATCH'])
@token_required
@validate_json_content_type
@use_args(user_update_schema, error_status_code=400)
def update_user_data(user_id: int, args: dict):

    if not isinstance(args, dict):
        abort(400, description="Invalid JSON body")

    if not args:
        abort(400, description="No data provided for update")

    user = db.session.get(User, user_id)
    if not user:
        abort(404, description=f'User with id {user_id} not found')

    if 'username' in args:
        user.username = args['username']
    if 'email' in args:
        user.email = args['email']

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Username or email already in use")

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    }), 200


