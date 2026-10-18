import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db, limiter
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@auth_bp.route("/auth/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    """Registers a new user account and returns a JWT access token."""
    data = request.get_json(silent=True) or {}

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Validation
    errors = []
    if not full_name:
        errors.append({"field": "full_name", "message": "Full name is required."})
    if not email or not EMAIL_REGEX.match(email):
        errors.append({"field": "email", "message": "A valid email address is required."})
    if not password or len(password) < 8:
        errors.append({"field": "password", "message": "Password must be at least 8 characters long."})

    if errors:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "data": None,
            "errors": errors,
        }), 400

    # Check for duplicate email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({
            "success": False,
            "message": "An account with this email address already exists.",
            "data": None,
            "errors": [{"field": "email", "message": "Email is already registered."}],
        }), 409

    # Create new user
    user = User(full_name=full_name, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    # Generate JWT token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "success": True,
        "message": "Account created successfully.",
        "data": {
            "user": user.to_dict(),
            "access_token": access_token,
        },
        "errors": None,
    }), 201

@auth_bp.route("/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    """Authenticates a user with email and password and returns a JWT access token."""
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Both email and password are required.",
            "data": None,
            "errors": None,
        }), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password.",
            "data": None,
            "errors": None,
        }), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "data": {
            "user": user.to_dict(),
            "access_token": access_token,
        },
        "errors": None,
    }), 200

@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    """Client-side token teardown confirmation."""
    return jsonify({
        "success": True,
        "message": "Successfully logged out.",
        "data": None,
        "errors": None,
    }), 200

