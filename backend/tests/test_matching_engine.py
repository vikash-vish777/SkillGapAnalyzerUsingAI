import io
import pytest
import pymupdf
from app import create_app
from app.extensions import db
from app.models.job_role import JobRole
from app.models.skill import Skill
from app.models.job_required_skill import JobRequiredSkill
from app.ai.extractor import SkillExtractor
from app.services.matching_engine import SkillMatchingEngine

@pytest.fixture
def test_app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()

        # Seed test skills
        python_skill = Skill(name="Python", normalized_name="python", category="Programming Language")
        react_skill = Skill(name="React.js", normalized_name="react.js", category="Frontend")
        docker_skill = Skill(name="Docker", normalized_name="docker", category="DevOps")
        sql_skill = Skill(name="SQL", normalized_name="sql", category="Database")
        aws_skill = Skill(name="AWS", normalized_name="aws", category="Cloud")
        db.session.add_all([python_skill, react_skill, docker_skill, sql_skill, aws_skill])
        db.session.commit()

        # Seed role
        role = JobRole(title="Full Stack Developer", category="Software Engineering")
        db.session.add(role)
        db.session.commit()

        # Requirements: Python (essential, wt 2.0), React (essential, wt 2.0), Docker (preferred, wt 1.0)
        req1 = JobRequiredSkill(job_role_id=role.id, skill_id=python_skill.id, importance_weight=2.0, requirement_type="essential")
        req2 = JobRequiredSkill(job_role_id=role.id, skill_id=react_skill.id, importance_weight=2.0, requirement_type="essential")
        req3 = JobRequiredSkill(job_role_id=role.id, skill_id=docker_skill.id, importance_weight=1.0, requirement_type="preferred")
        db.session.add_all([req1, req2, req3])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

def test_alias_extraction_resolution():
    """Verify that different aliases resolve to canonical skill names."""
    extractor = SkillExtractor()
    sample_text = (
        "Frontend built using ReactJS and JS. Backend written in Python3 with Flask API. "
        "Containerized using Docker Compose and deployed to k8s."
    )
    extracted = extractor.extract_skills(sample_text)

    assert "React.js" in extracted
    assert "JavaScript" in extracted
    assert "Python" in extracted
    assert "Flask" in extracted
    assert "Docker" in extracted
    assert "Kubernetes" in extracted

def test_prevent_false_positive_collisions():
    """Verify that single-letter 'C' is not matched inside words like 'Basic' or 'Cloud'."""
    extractor = SkillExtractor()
    non_c_text = "Basic understanding of Cloud computing, Cascading stylesheets, and Go-to-market strategies."
    extracted = extractor.extract_skills(non_c_text)

    # Should NOT extract 'C' as a programming language from 'Cloud' or 'Basic'
    assert "C" not in extracted

def test_evidence_snippet_capture():
    """Verify that the sentence containing the skill is preserved as audit evidence."""
    extractor = SkillExtractor()
    text = (
        "Education: Bachelor of Science.\n"
        "Experience: Architected microservices with Python and Docker for healthcare clients.\n"
        "Awards: Top contributor 2025."
    )
    extracted = extractor.extract_skills(text)

    assert "Python" in extracted
    assert "Architected microservices" in extracted["Python"]["evidence"]
    assert "Docker" in extracted
    assert "healthcare clients" in extracted["Docker"]["evidence"]

def test_matching_engine_basic_and_weighted_scores():
    """Test standard and weighted match score calculations."""
    candidate_skills = [
        {"name": "Python", "skill_id": 1, "category": "Programming Language", "evidence": "Used Python"},
        {"name": "React.js", "skill_id": 2, "category": "Frontend", "evidence": "Built React app"},
        {"name": "MongoDB", "skill_id": 99, "category": "Database", "evidence": "Used MongoDB"},  # Additional
    ]

    role_requirements = [
        {"skill_name": "Python", "skill_id": 1, "importance_weight": 2.0, "requirement_type": "essential"},
        {"skill_name": "React.js", "skill_id": 2, "importance_weight": 2.0, "requirement_type": "essential"},
        {"skill_name": "Docker", "skill_id": 3, "importance_weight": 1.0, "requirement_type": "preferred"},
    ]

    result = SkillMatchingEngine.compare_skills(candidate_skills, role_requirements)

    # Total required: 3. Matched: 2 (Python, React.js). Missing: 1 (Docker).
    # Basic Match % = (2 / 3) * 100 = 66.67%
    assert result["total_required_count"] == 3
    assert result["matched_count"] == 2
    assert result["missing_count"] == 1
    assert result["match_percentage"] == 66.67

    # Total weight: 2.0 + 2.0 + 1.0 = 5.0. Matched weight: 2.0 + 2.0 = 4.0.
    # Weighted Match % = (4.0 / 5.0) * 100 = 80.0%
    assert result["weighted_match_percentage"] == 80.0

    # Check gap breakdown
    assert len(result["essential_missing_skills"]) == 0
    assert len(result["preferred_missing_skills"]) == 1
    assert result["preferred_missing_skills"][0]["name"] == "Docker"

    # Check additional skills
    assert len(result["additional_skills"]) == 1
    assert result["additional_skills"][0]["name"] == "MongoDB"

def test_matching_engine_zero_requirements_edge_case():
    """Test that zero requirements are handled gracefully without division by zero."""
    result = SkillMatchingEngine.compare_skills([], [])
    assert result["match_percentage"] == 100.0
    assert result["weighted_match_percentage"] == 100.0
    assert result["matched_count"] == 0

def test_full_skill_gap_analysis_endpoint(client):
    """Test end-to-end POST /api/analyses with an in-memory PDF resume."""
    # Create sample PDF containing Python and React.js
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text(
        (50, 50),
        "Jane Developer\nFull Stack Engineer\nSkills: Python programming, React.js web apps, SQL databases."
    )
    pdf_bytes = doc.tobytes()
    doc.close()

    data = {
        "file": (io.BytesIO(pdf_bytes), "jane_resume.pdf"),
        "job_role_id": "1",
    }

    response = client.post(
        "/api/analyses",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    res_data = response.get_json()
    assert res_data["success"] is True
    analysis = res_data["data"]

    assert analysis["job_role"]["title"] == "Full Stack Developer"
    assert analysis["matched_count"] >= 2  # Python and React.js matched
    assert "Docker" in [s["name"] for s in analysis["preferred_missing_skills"]]
    assert analysis["match_percentage"] > 0
    assert analysis["algorithm_version"] == "v1.0"
