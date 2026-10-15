from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.job_role import JobRole

job_roles_bp = Blueprint("job_roles", __name__)

@job_roles_bp.route("/job-roles", methods=["GET"])
def get_job_roles():
    """Retrieve all available job roles with optional category filtering."""
    category = request.args.get("category")
    query = JobRole.query

    if category:
        query = query.filter(JobRole.category.ilike(f"%{category}%"))

    roles = query.order_by(JobRole.title.asc()).all()

    return jsonify({
        "success": True,
        "message": f"Retrieved {len(roles)} job roles.",
        "data": [role.to_dict(include_skills=False) for role in roles],
        "errors": None,
    }), 200

@job_roles_bp.route("/job-roles/<int:role_id>", methods=["GET"])
def get_job_role_by_id(role_id: int):
    """Retrieve specific job role details along with all required skills."""
    role = db.session.get(JobRole, role_id)
    if not role:
        return jsonify({
            "success": False,
            "message": f"Job role with ID {role_id} not found.",
            "data": None,
            "errors": None,
        }), 404

    return jsonify({
        "success": True,
        "message": "Job role retrieved successfully.",
        "data": role.to_dict(include_skills=True),
        "errors": None,
    }), 200
