from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from app.errors.exceptions import AppError

def register_error_handlers(app):
    """Registers standardized JSON error handlers for common HTTP status codes."""

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({
            "success": False,
            "message": error.message,
            "data": None,
            "errors": error.details if error.details else None
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        message = getattr(error, "description", "Bad Request")
        return jsonify({
            "success": False,
            "message": message,
            "data": None,
            "errors": None
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "message": "Authentication required or invalid token.",
            "data": None,
            "errors": None
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "message": "You do not have permission to access this resource.",
            "data": None,
            "errors": None
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Requested resource was not found.",
            "data": None,
            "errors": None
        }), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            "success": False,
            "message": "File exceeds the maximum allowed upload size (5MB).",
            "data": None,
            "errors": None
        }), 413

    @app.errorhandler(429)
    def ratelimit_handler(error):
        return jsonify({
            "success": False,
            "message": f"Rate limit exceeded: {error.description}",
            "data": None,
            "errors": None
        }), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "message": "An internal server error occurred. Please try again later.",
            "data": None,
            "errors": None
        }), 500

    @app.errorhandler(Exception)
    def handle_unhandled_exception(error):
        # Allow standard HTTP exceptions (400, 401, 403, 404, 429, etc.) to pass through
        if isinstance(error, HTTPException):
            return error

        current_app.logger.error(f"Unhandled Exception: {str(error)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "An internal server error occurred. Please try again later.",
            "data": None,
            "errors": None
        }), 500

