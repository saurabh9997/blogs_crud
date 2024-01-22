from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.factories.application import create_app

app = create_app()
CORS(app, expose_headers="*")
JWTManager(app)
Bcrypt(app)

if __name__ == '__main__':
    app.run()
