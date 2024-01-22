import os
import uuid
from datetime import datetime

from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy

from app.blueprints.error_handlers.errors import errors_blueprint
from app.settings import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.register_blueprint(errors_blueprint)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logisticsnow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()
    from app.blueprints.auth.api import auth_blueprint
    from app.blueprints.blogs.api import blog_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/api")
    app.register_blueprint(blog_blueprint, url_prefix="/api")

    config_name = os.getenv('ENVIRONMENT')
    if not config_name:
        raise Exception("Environment Not Found")
    app.config.from_object(config.app_config[config_name])

    @app.before_request
    def set_start_time():
        g.start_time = datetime.now()

    @app.after_request
    def set_default_content_type(response):
        response.headers['content-type'] = "application/json"
        return response

    @app.after_request
    def log_response(response):
        request_id = request.environ['REQUEST_ID'] if 'REQUEST_ID' in request.environ.keys() else uuid.uuid4().hex[:8]
        session_id = request.environ['SESSION_ID'] if 'SESSION_ID' in request.environ.keys() else uuid.uuid4().hex[:8]

        start_time = g.start_time
        end_time = datetime.now()
        diff = end_time - start_time
        diff_in_ms = int(diff.total_seconds() * 1000)

        if response.status_code in [200, 201]:
            print("{} {} {} {} {} {} {} {} {}".format(request.remote_addr, request_id, session_id, request.method,
                request.path, response.status_code, diff_in_ms, "ms", "{}"))
        else:
            print("{} {} {} {} {} {} {} {} {}".format(request.remote_addr, request_id, session_id, request.method,
                request.path, response.status_code, diff_in_ms, "ms", response.json))
        return response

    return app
