import os
from flask import Flask
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors, limiter
from app.errors.handlers import register_error_handlers
from app.routes.health import health_bp
from app.routes.job_roles import job_roles_bp
from app.routes.resumes import resumes_bp
from app.routes.analyses import analyses_bp
from app.routes.auth import auth_bp
from app.routes.users import users_bp

# Import models so SQLAlchemy and Alembic register all entities
import app.models  # noqa: F401

def create_app(config_name=None):
    """Application factory for Skill Gap Analyzer API."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    
    # Configure CORS with explicit allowed origins
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}},
        supports_credentials=True,
    )

    # Register standardized error handlers
    register_error_handlers(app)

    # Enforce standard security headers on all responses
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    # Register blueprints with /api prefix
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(job_roles_bp, url_prefix="/api")
    app.register_blueprint(resumes_bp, url_prefix="/api")
    app.register_blueprint(analyses_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api")

    return app
