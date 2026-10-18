import io
import pytest
import pymupdf
from app import create_app
from app.extensions import db
from app.models.job_role import JobRole
from app.models.skill import Skill
from app.models.job_required_skill import JobRequiredSkill
from app.services.recommendation_service import RecommendationService
from app.services.career_advisor import CareerAdvisorService
from app.ai.semantic_matcher import SemanticMatcher

@pytest.fixture
def app_with_roles():
    app = create_app("testing")
    with app.app_context():
        db.create_all()

        # Seed skills
        py = Skill(name="Python", normalized_name="python", category="Programming Language")
        react = Skill(name="React.js", normalized_name="react.js", category="Frontend")
        js = Skill(name="JavaScript", normalized_name="javascript", category="Programming Language")
        docker = Skill(name="Docker", normalized_name="docker", category="DevOps")
        k8s = Skill(name="Kubernetes", normalized_name="kubernetes", category="DevOps")
        db.session.add_all([py, react, js, docker, k8s])
        db.session.commit()

        # Role 1: Backend Engineer
        backend_role = JobRole(title="Backend Engineer", category="Backend")
        db.session.add(backend_role)
        db.session.commit()
        db.session.add_all([
            JobRequiredSkill(job_role_id=backend_role.id, skill_id=py.id, importance_weight=1.5, requirement_type="essential"),
            JobRequiredSkill(job_role_id=backend_role.id, skill_id=docker.id, importance_weight=1.2, requirement_type="essential"),
            JobRequiredSkill(job_role_id=backend_role.id, skill_id=k8s.id, importance_weight=1.0, requirement_type="preferred"),
        ])

        # Role 2: Frontend Engineer
        frontend_role = JobRole(title="Frontend Engineer", category="Frontend")
        db.session.add(frontend_role)
        db.session.commit()
        db.session.add_all([
            JobRequiredSkill(job_role_id=frontend_role.id, skill_id=react.id, importance_weight=1.8, requirement_type="essential"),
            JobRequiredSkill(job_role_id=frontend_role.id, skill_id=js.id, importance_weight=1.5, requirement_type="essential"),
        ])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_with_roles):
    return app_with_roles.test_client()

def test_recommendation_generation(app_with_roles):
    """Test that missing skills produce structured learning roadmaps."""
    missing = [
        {"name": "Docker", "skill_id": 4, "requirement_type": "essential"},
        {"name": "Kubernetes", "skill_id": 5, "requirement_type": "preferred"},
    ]
    recs = RecommendationService.generate_recommendations(missing)

    assert len(recs) == 2
    # Essential Docker should be Priority 1
    assert recs[0]["skill_name"] == "Docker"
    assert recs[0]["priority"] == 1
    assert "topics" in str(recs[0]["recommended_topics"]).lower() or len(recs[0]["recommended_topics"]) > 0
    assert "compose" in recs[0]["practice_exercise"].lower()

    # Preferred Kubernetes should be Priority 2
    assert recs[1]["skill_name"] == "Kubernetes"
    assert recs[1]["priority"] == 2

def test_career_advisor_alternative_suggestions(app_with_roles):
    """Test recommending Frontend Engineer when candidate has React and JavaScript skills."""
    candidate_skills = [
        {"name": "React.js", "category": "Frontend"},
        {"name": "JavaScript", "category": "Programming Language"},
    ]

    # Candidate targeted role 1 (Backend Engineer), so Frontend Engineer should be suggested
    alternatives = CareerAdvisorService.recommend_alternative_roles(
        candidate_skills,
        current_job_role_id=1,
        min_overlap_threshold=40.0
    )

    assert len(alternatives) >= 1
    suggested = alternatives[0]
    assert suggested["title"] == "Frontend Engineer"
    assert suggested["match_percentage"] == 100.0  # Has React and JS
    assert "Frontend Engineer" in suggested["recommendation_reason"]
    assert "disclaimer" in suggested

def test_semantic_matcher_similarity():
    """Test TF-IDF cosine similarity between resume and job description."""
    resume = "Experienced software developer skilled in Python microservices, Flask APIs, and Docker containerization."
    job_desc = "Seeking a Python Engineer to develop scalable Flask REST services and manage Docker deployments."

    result = SemanticMatcher.compute_similarity(resume, job_desc)
    assert result["similarity_score"] > 0.1
    assert result["similarity_percentage"] > 10.0
    assert "Semantic Alignment" in result["interpretation"]
    assert any("python" in k or "flask" in k or "docker" in k for k in result["shared_keywords"])

def test_full_analysis_with_recommendations_and_careers(client):
    """Test POST /api/analyses returns recommendations, career roles, and semantic similarity."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Jane Doe\nSkills: Python, React.js, JavaScript.")
    pdf_bytes = doc.tobytes()
    doc.close()

    data = {
        "file": (io.BytesIO(pdf_bytes), "jane.pdf"),
        "job_role_id": "1",  # Backend Engineer (requires Python, Docker, Kubernetes)
    }

    response = client.post("/api/analyses", data=data, content_type="multipart/form-data")
    assert response.status_code == 200

    payload = response.get_json()["data"]
    # Check recommendation presence for missing Docker and Kubernetes
    assert "recommendations" in payload
    missing_skill_names = [r["skill_name"] for r in payload["recommendations"]]
    assert "Docker" in missing_skill_names

    # Check alternative career suggestions (should suggest Frontend Engineer since she has React & JS)
    assert "suggested_career_roles" in payload
    assert len(payload["suggested_career_roles"]) >= 1
    assert payload["suggested_career_roles"][0]["title"] == "Frontend Engineer"

    # Check semantic similarity report
    assert "semantic_similarity" in payload
    assert payload["semantic_similarity"]["similarity_score"] > 0

