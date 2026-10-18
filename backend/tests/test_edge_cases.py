import io
import pytest
import pymupdf
from app import create_app
from app.extensions import db, limiter
from app.models.job_role import JobRole
from app.models.skill import Skill
from app.models.job_required_skill import JobRequiredSkill
from app.models.learning_resource import LearningResource

@pytest.fixture
def app_with_test_data():
    """Sets up an isolated test app with a full job role and database schema."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()

        # Seed skills
        skills = {
            "python": Skill(name="Python", normalized_name="python", category="Programming Language"),
            "sql": Skill(name="SQL", normalized_name="sql", category="Database"),
            "docker": Skill(name="Docker", normalized_name="docker", category="DevOps"),
            "fastapi": Skill(name="FastAPI", normalized_name="fastapi", category="Web Framework"),
        }
        for s in skills.values():
            db.session.add(s)
        db.session.commit()

        # Seed learning resources for Python & Docker
        res1 = LearningResource(
            skill_id=skills["python"].id,
            title="Official Python Tutorial",
            description="Complete Python reference and exercises",
            resource_url="https://docs.python.org/3/tutorial/",
            resource_type="documentation",
            difficulty_level="beginner"
        )
        res2 = LearningResource(
            skill_id=skills["docker"].id,
            title="Docker Getting Started",
            description="Guide to containerizing apps",
            resource_url="https://docs.docker.com/get-started/",
            resource_type="tutorial",
            difficulty_level="intermediate"
        )
        db.session.add_all([res1, res2])

        # Seed target job role: "Python Developer"
        role = JobRole(
            title="Python Developer",
            category="Backend",
            description="Build scalable APIs and microservices using Python, SQL, Docker, and FastAPI."
        )
        db.session.add(role)
        db.session.commit()

        # Seed required skills: Python (essential, wt 2.0), SQL (essential, wt 1.5), Docker (preferred, wt 1.0), FastAPI (preferred, wt 1.0)
        reqs = [
            JobRequiredSkill(job_role_id=role.id, skill_id=skills["python"].id, importance_weight=2.0, requirement_type="essential"),
            JobRequiredSkill(job_role_id=role.id, skill_id=skills["sql"].id, importance_weight=1.5, requirement_type="essential"),
            JobRequiredSkill(job_role_id=role.id, skill_id=skills["docker"].id, importance_weight=1.0, requirement_type="preferred"),
            JobRequiredSkill(job_role_id=role.id, skill_id=skills["fastapi"].id, importance_weight=1.0, requirement_type="preferred"),
        ]
        db.session.add_all(reqs)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_with_test_data):
    return app_with_test_data.test_client()

def test_non_technical_resume_zero_skills(client):
    """Test non-technical resume (e.g. recipe) produces 0.0% match with no division-by-zero or crash."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text(
        (50, 50),
        "Grandma's recipe for homemade pasta: Blend semolina flour, farm-fresh eggs, extra virgin olive oil, and sea salt. "
        "Knead the mixture vigorously for ten minutes until silky smooth, rest covered for thirty minutes, then roll into tagliatelle noodles."
    )
    pdf_bytes = doc.tobytes()
    doc.close()

    response = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(pdf_bytes), "pasta_recipe.pdf"),
            "job_role_id": "1",
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["match_percentage"] == 0.0
    assert data["weighted_match_percentage"] == 0.0
    assert len(data["matched_skills"]) == 0
    assert len(data["missing_skills"]) == 4
    assert len(data["essential_missing_skills"]) == 2  # Python and SQL
    assert len(data["preferred_missing_skills"]) == 2  # Docker and FastAPI
    assert len(data["recommendations"]) == 4
    assert data["semantic_similarity"]["similarity_score"] >= 0.0

def test_perfect_match_candidate_100_percent(client):
    """Test candidate possessing 100% of required skills scores 100.0% with zero missing skills."""
    # Register user first so we can also test report generation
    reg = client.post("/api/auth/register", json={
        "full_name": "Perfect Candidate",
        "email": "perfect@example.com",
        "password": "Password123!"
    })
    token = reg.get_json()["data"]["access_token"]

    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text(
        (50, 50),
        "Senior Software Engineer specializing in Python, SQL, Docker, and FastAPI development. "
        "Experienced in architecting REST APIs with FastAPI, managing databases with SQL queries, "
        "and deploying containerized microservices via Docker."
    )
    pdf_bytes = doc.tobytes()
    doc.close()

    response = client.post(
        "/api/analyses",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "file": (io.BytesIO(pdf_bytes), "perfect_candidate.pdf"),
            "job_role_id": "1",
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["match_percentage"] == 100.0
    assert data["weighted_match_percentage"] == 100.0
    assert len(data["matched_skills"]) == 4
    assert len(data["missing_skills"]) == 0
    assert len(data["essential_missing_skills"]) == 0
    assert len(data["preferred_missing_skills"]) == 0
    assert data["semantic_similarity"]["interpretation"] == "High Semantic Alignment"
    analysis_id = data["id"]

    # Verify PDF report generation succeeds for 100% match
    report_res = client.get(
        f"/api/analyses/{analysis_id}/report",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert report_res.status_code == 200
    assert report_res.headers["Content-Type"] == "application/pdf"
    assert report_res.data.startswith(b"%PDF-")

def test_corrupted_pdf_handling(client):
    """Test corrupted PDF file returns HTTP 400 with descriptive error message."""
    # Corrupt payload: starts with %PDF- header but contains invalid binary junk
    corrupted_bytes = b"%PDF-1.4\n" + b"\x00\xff\xfe\xca\xfe\xba\xbe" * 20
    response = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(corrupted_bytes), "corrupt.pdf"),
            "job_role_id": "1",
        },
        content_type="multipart/form-data"
    )
    assert response.status_code in (400, 422)
    json_data = response.get_json()
    assert json_data["success"] is False
    assert "error" in json_data["message"].lower() or "failed" in json_data["message"].lower() or "text" in json_data["message"].lower()

def test_zero_byte_file_rejected(client):
    """Test 0-byte file is rejected with HTTP 400."""
    response = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(b""), "empty.pdf"),
            "job_role_id": "1",
        },
        content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert "0 bytes" in response.get_json()["message"]

def test_executable_disguised_as_pdf_rejected(client):
    """Test executable binary renamed to .pdf is rejected by magic byte detection."""
    fake_exe = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff" + b"A" * 100
    response = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(fake_exe), "malware.pdf"),
            "job_role_id": "1",
        },
        content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert "Executable content detected" in response.get_json()["message"]

def test_unsupported_file_extension(client):
    """Test files with unapproved extensions (.txt, .exe, .png) are rejected."""
    response = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(b"Some plain text resume"), "resume.txt"),
            "job_role_id": "1",
        },
        content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.get_json()["message"]

def test_file_too_large_rejection(client):
    """Test file exceeding 5MB limit is rejected."""
    oversized_data = b"%PDF-" + b"0" * (6 * 1024 * 1024)  # 6MB
    response = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(oversized_data), "huge_resume.pdf"),
            "job_role_id": "1",
        },
        content_type="multipart/form-data"
    )
    # Exceeding limit will trigger DocumentService 400 or Flask 413
    assert response.status_code in (400, 413)

def test_invalid_job_role_id_boundaries(client):
    """Test non-existent and non-numeric job role IDs are handled cleanly."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Jane Doe - Python engineer with SQL knowledge.")
    pdf_bytes = doc.tobytes()
    doc.close()

    # Non-existent job role ID
    res_404 = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(pdf_bytes), "resume.pdf"),
            "job_role_id": "99999",
        },
        content_type="multipart/form-data"
    )
    assert res_404.status_code == 404
    assert "not found" in res_404.get_json()["message"].lower()

    # Non-numeric job role ID
    res_400 = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(pdf_bytes), "resume.pdf"),
            "job_role_id": "abc_not_an_int",
        },
        content_type="multipart/form-data"
    )
    assert res_400.status_code == 400
    assert "integer" in res_400.get_json()["message"].lower()

def test_custom_job_description_with_obscure_terms(client):
    """Test analysis using a custom job description containing rare/obscure keywords and unicode."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Jane Doe - Python developer experienced with Docker containers.")
    pdf_bytes = doc.tobytes()
    doc.close()

    custom_jd = (
        "We are looking for an expert in QuantumFlux-9, HyperSpaceDB, and 🚀 cosmic streaming. "
        "Candidates should have basic understanding of Python."
    )

    response = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(pdf_bytes), "resume.pdf"),
            "job_role_id": "1",
            "custom_job_description": custom_jd,
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert "semantic_similarity" in data
    # Semantic similarity should complete cleanly without errors
    assert isinstance(data["semantic_similarity"]["similarity_score"], float)
    assert 0.0 <= data["semantic_similarity"]["similarity_score"] <= 1.0

def test_auth_rate_limiting_enforcement():
    """Test that rapid consecutive authentication attempts trigger HTTP 429 Too Many Requests."""
    app = create_app("testing")
    app.config["RATELIMIT_ENABLED"] = True
    app.config["RATELIMIT_STORAGE_URI"] = "memory://"
    limiter.init_app(app)
    limiter.enabled = True

    with app.app_context():
        db.create_all()

    rate_client = app.test_client()

    # Make 5 attempts (configured limit is 5 per minute)
    for _ in range(5):
        res = rate_client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "wrongpassword123"}
        )
        assert res.status_code == 401

    # 6th attempt should be blocked with HTTP 429
    blocked_res = rate_client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword123"}
    )
    assert blocked_res.status_code == 429
    json_data = blocked_res.get_json()
    assert json_data["success"] is False
    assert "Rate limit exceeded" in json_data["message"]

def test_security_headers_present_on_responses(client):
    """Test all responses include standard defensive HTTP security headers."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

def test_jwt_tampering_and_unauthorized_access(client):
    """Test unauthenticated and tampered JWT requests are rejected with 401 or 422."""
    # 1. No token provided
    res_no_token = client.get("/api/users/me")
    assert res_no_token.status_code == 401

    # 2. Forged / invalid token
    res_bad_token = client.get(
        "/api/users/me",
        headers={"Authorization": "Bearer totally.invalid.tampered.token"}
    )
    assert res_bad_token.status_code in (401, 422)
