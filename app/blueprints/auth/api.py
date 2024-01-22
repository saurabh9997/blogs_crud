# app/blueprints/api.py

from datetime import timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from app.blueprints.auth.serializers import UserSchema
from app.blueprints.auth.service import get_user_by_username, register_user
from app.factories.application import db

auth_blueprint = Blueprint('auth', __name__)
user_schema = UserSchema()


@auth_blueprint.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Returns:
        JSON response indicating the success of the user registration.
    """
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify({'error': 'Validation error', 'message': errors}), 400

    message, status = register_user(data)
    return jsonify(message), status


@auth_blueprint.route('/login', methods=['POST'])
def login_user():
    """
    Log in an existing user and obtain a JWT token for authentication.

    Returns:
        JSON response containing the JWT token for the authenticated user.
    """
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Invalid credentials'}), 401

    user = get_user_by_username(auth.username)
    if not user or not check_password_hash(user.password, auth.password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = create_access_token(identity=auth.username, expires_delta=timedelta(days=1))
    return jsonify({'token': token}), 200


@auth_blueprint.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """
    Change the password of the authenticated user.

    Returns:
        JSON response indicating the success of the password change.
    """
    current_user = get_jwt_identity()
    user = get_user_by_username(current_user)

    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not check_password_hash(user.password, old_password):
        return jsonify({'message': 'Invalid old password'}), 401

    user.password = generate_password_hash(new_password, method='sha256')
    db.session.commit()

    return jsonify({'message': 'Password changed successfully!'}), 200
