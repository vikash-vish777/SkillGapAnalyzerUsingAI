from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.analysis import Analysis

users_bp = Blueprint("users", __name__)

@users_bp.route("/users/me", methods=["GET"])
@jwt_required()
def get_current_user_profile():
    """Retrieves authenticated user profile information."""
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user:
        return jsonify({
            "success": False,
            "message": "User account not found.",
            "data": None,
            "errors": None,
        }), 404

    return jsonify({
        "success": True,
        "message": "User profile retrieved successfully.",
        "data": user.to_dict(),
        "errors": None,
    }), 200

@users_bp.route("/users/dashboard", methods=["GET"])
@jwt_required(optional=True)
def get_dashboard_summary():
    """Returns analytics dashboard metrics for the authenticated user (or default demo metrics)."""
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id)) if user_id else None

    if not user:
        # Default empty summary for unauthenticated visitors
        return jsonify({
            "success": True,
            "message": "Dashboard data retrieved.",
            "data": {
                "total_analyses": 0,
                "latest_match_percentage": None,
                "average_match_percentage": None,
                "recent_analyses": [],
            },
            "errors": None,
        }), 200

    analyses = (
        Analysis.query.filter_by(user_id=user.id)
        .order_by(Analysis.created_at.desc())
        .limit(5)
        .all()
    )

    total_count = Analysis.query.filter_by(user_id=user.id).count()

    scores = [float(a.match_percentage) for a in analyses if a.match_percentage is not None]
    avg_score = round(sum(scores) / len(scores), 2) if scores else None
    latest_score = float(analyses[0].match_percentage) if analyses else None

    return jsonify({
        "success": True,
        "message": "Dashboard metrics retrieved successfully.",
        "data": {
            "total_analyses": total_count,
            "latest_match_percentage": latest_score,
            "average_match_percentage": avg_score,
            "recent_analyses": [a.to_dict(include_details=False) for a in analyses],
        },
        "errors": None,
    }), 200
