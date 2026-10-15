import os
from flask import Flask
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors, limiter
from app.errors.handlers import register_error_handlers
from app.routes.health import health_bp

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

    # Register blueprints with /api prefix
    app.register_blueprint(health_bp, url_prefix="/api")

    return app
