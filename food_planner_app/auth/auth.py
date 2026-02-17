from flask import abort, jsonify
from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import use_args

from food_planner_app import db
from food_planner_app.auth import auth_bp
from food_planner_app.models import (
    User,
    UserSchema,
    user_password_update_schema,
    user_schema,
    user_update_schema,
)
from food_planner_app.utils import token_required, validate_json_content_type


@auth_bp.route('/register', methods=['POST'])
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    """
    Register a new user
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: piotr
            email:
              type: string
              example: piotr@test.com
            password:
              type: string
              example: "123456"
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            token:
              type: string
      400:
        description: Validation error
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: User with username piotr already exists
      409:
        description: User already exists
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: User with username piotr already exists
    """
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
    """
    Login user
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: piotr
            password:
              type: string
              example: "123456"
    responses:
      200:
        description: JWT token returned
        schema:
          type: object
          properties:
            success:
              type: boolean
            token:
              type: string
      400:
        description: Validation error
      401:
        description: Invalid credentials
    """
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
    """
    Get current authenticated user
    ---
    tags:
      - Authentication
    produces:
      - application/json
    security:
      - BearerAuth: []
    responses:
      200:
        description: Current user data
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                email:
                  type: string
      401:
        description: Unauthorized
      404:
        description: User not found
    """
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
    """
    Update user password
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - current_password
            - new_password
          properties:
            current_password:
              type: string
              example: "123456"
            new_password:
              type: string
              example: "newStrongPassword"
    responses:
      200:
        description: Password updated successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
      400:
        description: Validation error
      401:
        description: Invalid password
      404:
        description: User not found
    """
    user = db.session.get(User, user_id)
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
    """
    Update user data
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: new_username
            email:
              type: string
              example: new_email@test.com
    responses:
      200:
        description: User data updated
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
      400:
        description: Invalid request body
      401:
        description: Unauthorized
      404:
        description: User not found
      409:
        description: Username or email already in use
    """

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

