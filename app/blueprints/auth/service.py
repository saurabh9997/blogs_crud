from flask_bcrypt import generate_password_hash

from app.blueprints.auth.models.user import User
from app.factories.application import db


def register_user(auth_data):
    """
    Register a new user.

    Args:
        auth_data (dict): Authentication data containing username and password.

    Returns:
        tuple: A tuple containing a response message and HTTP status code.
    """
    username = auth_data.get("username")
    password = auth_data.get('password')
    existing_user = get_user_by_username(username)

    if existing_user:
        return {'message': 'User already exists!'}, 400

    if create_user(username, password):
        return {'message': 'User registered successfully!'}, 200


def get_user_by_username(username):
    """
    Retrieve a user by their username.

    Args:
        username (str): The username of the user.

    Returns:
        User or None: The user with the specified username or None if not found.
    """
    return User.query.filter_by(username=username).first()


def create_user(username, password):
    """
    Create a new user.

    Args:
        username (str): The username of the new user.
        password (str): The plaintext password of the new user.

    Returns:
        bool: True if the user is successfully created, False otherwise.
    """
    if username and password:
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return True
    return False
