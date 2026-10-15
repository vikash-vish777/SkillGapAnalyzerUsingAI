from flask import Blueprint, jsonify
from sqlalchemy import text
from app.extensions import db

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify backend operational readiness and DB status."""
    db_status = "disconnected"
    try:
        # Ping the database with a lightweight query
        db.session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as exc:
        db_status = f"unreachable: {str(exc)}"

    return jsonify({
        "success": True,
        "message": "Skill Gap Analyzer API is operational",
        "data": {
            "status": "UP",
            "database": db_status,
            "version": "1.0.0"
        },
        "errors": None
    }), 200
