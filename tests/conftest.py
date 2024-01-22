import pytest
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.factories.application import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


# Fixture to provide a test client for the Flask app
@pytest.fixture
def client(app):
    return app.test_client()


# Fixture to provide a test database session
@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
