import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.job_role import JobRole
from app.models.skill import Skill
from app.models.job_required_skill import JobRequiredSkill
from app.models.learning_resource import LearningResource

@pytest.fixture
def app_with_db():
    """Provides an isolated in-memory test application and database context."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()

        # Seed minimal test fixtures
        skill1 = Skill(name="Python", normalized_name="python", category="Programming Language")
        skill2 = Skill(name="React.js", normalized_name="react.js", category="Frontend")
        db.session.add_all([skill1, skill2])
        db.session.commit()

        resource = LearningResource(
            skill_id=skill1.id,
            title="Official Python Docs",
            resource_url="https://docs.python.org",
            resource_type="documentation",
            difficulty_level="beginner"
        )
        db.session.add(resource)

        role = JobRole(title="Software Engineer", category="Engineering", description="General engineering role")
        db.session.add(role)
        db.session.commit()

        req = JobRequiredSkill(
            job_role_id=role.id,
            skill_id=skill1.id,
            importance_weight=1.5,
            requirement_type="essential"
        )
        db.session.add(req)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_with_db):
    return app_with_db.test_client()

def test_user_password_hashing(app_with_db):
    """Test bcrypt hashing and verification on User model."""
    user = User(full_name="Alice Smith", email="alice@example.com")
    user.set_password("SecurePassword999!")

    assert user.password_hash != "SecurePassword999!"
    assert user.check_password("SecurePassword999!") is True
    assert user.check_password("WrongPassword") is False

    user_dict = user.to_dict()
    assert "password_hash" not in user_dict
    assert user_dict["email"] == "alice@example.com"

def test_get_job_roles_endpoint(client):
    """Test GET /api/job-roles returns list of seeded roles."""
    response = client.get("/api/job-roles")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) >= 1
    assert data["data"][0]["title"] == "Software Engineer"

def test_get_job_role_detail_endpoint(client):
    """Test GET /api/job-roles/<id> returns role with its required skills."""
    response = client.get("/api/job-roles/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    role = data["data"]
    assert role["title"] == "Software Engineer"
    assert "required_skills" in role
    assert len(role["required_skills"]) == 1
    assert role["required_skills"][0]["skill_name"] == "Python"

def test_get_job_role_not_found(client):
    """Test GET /api/job-roles/999 returns 404 JSON error."""
    response = client.get("/api/job-roles/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert "not found" in data["message"].lower()

