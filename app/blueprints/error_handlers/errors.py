# app/blueprints/blogs/blog_blueprint.py

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

errors_blueprint = Blueprint('errors', __name__)


# Error handlers for API routes
@errors_blueprint.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400


@errors_blueprint.errorhandler(401)
def unauthorized_error(error):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401


@errors_blueprint.errorhandler(403)
def forbidden_error(error):
    return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to access this resource'}), 403


@errors_blueprint.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found'}), 404


@errors_blueprint.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500


# Global error handler for other exceptions
@errors_blueprint.errorhandler(Exception)
def handle_exception(error):
    return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500

