import io
import pytest
import pymupdf
from app import create_app
from app.extensions import db
from app.models.job_role import JobRole
from app.models.skill import Skill
from app.models.job_required_skill import JobRequiredSkill
from app.models.analysis import Analysis

@pytest.fixture
def app_with_users_and_role():
    app = create_app("testing")
    with app.app_context():
        db.create_all()

        # Seed skill & role
        skill = Skill(name="Python", normalized_name="python", category="Programming Language")
        db.session.add(skill)
        db.session.commit()

        role = JobRole(title="Python Developer", category="Backend")
        db.session.add(role)
        db.session.commit()

        req = JobRequiredSkill(job_role_id=role.id, skill_id=skill.id, importance_weight=1.5, requirement_type="essential")
        db.session.add(req)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_with_users_and_role):
    return app_with_users_and_role.test_client()

def test_authenticated_analysis_persistence(client):
    """Test that authenticated resume analysis persists records into the database."""
    # 1. Register User A
    reg = client.post("/api/auth/register", json={
        "full_name": "User Alpha",
        "email": "alpha@example.com",
        "password": "Password123!"
    })
    token_a = reg.get_json()["data"]["access_token"]

    # 2. Upload resume
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Jane Doe - Python Developer with Flask and SQL experience.")
    pdf_bytes = doc.tobytes()
    doc.close()

    response = client.post(
        "/api/analyses",
        data={
            "file": (io.BytesIO(pdf_bytes), "alpha_resume.pdf"),
            "job_role_id": "1",
        },
        headers={"Authorization": f"Bearer {token_a}"},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    res_data = response.get_json()["data"]
    assert res_data["id"] is not None
    analysis_id = res_data["id"]

    # 3. Verify user's analyses history list
    hist_res = client.get("/api/analyses", headers={"Authorization": f"Bearer {token_a}"})
    assert hist_res.status_code == 200
    hist_list = hist_res.get_json()["data"]
    assert len(hist_list) == 1
    assert hist_list[0]["id"] == analysis_id

    # 4. Verify user can retrieve analysis detail
    detail_res = client.get(f"/api/analyses/{analysis_id}", headers={"Authorization": f"Bearer {token_a}"})
    assert detail_res.status_code == 200
    assert detail_res.get_json()["data"]["id"] == analysis_id

    # 5. Verify PDF report download
    pdf_res = client.get(f"/api/analyses/{analysis_id}/report", headers={"Authorization": f"Bearer {token_a}"})
    assert pdf_res.status_code == 200
    assert pdf_res.headers["Content-Type"] == "application/pdf"
    assert pdf_res.data.startswith(b"%PDF-")

def test_user_data_isolation_security(client):
    """Test that User B cannot access User A's analysis report (HTTP 403 Forbidden)."""
    # Register User A and create an analysis
    reg_a = client.post("/api/auth/register", json={
        "full_name": "User Alpha",
        "email": "alpha2@example.com",
        "password": "Password123!"
    })
    token_a = reg_a.get_json()["data"]["access_token"]

    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Alpha Resume - Python experience.")
    pdf_bytes = doc.tobytes()
    doc.close()

    res = client.post(
        "/api/analyses",
        data={"file": (io.BytesIO(pdf_bytes), "alpha.pdf"), "job_role_id": "1"},
        headers={"Authorization": f"Bearer {token_a}"},
        content_type="multipart/form-data"
    )
    analysis_id = res.get_json()["data"]["id"]

    # Register User B
    reg_b = client.post("/api/auth/register", json={
        "full_name": "User Beta",
        "email": "beta@example.com",
        "password": "Password123!"
    })
    token_b = reg_b.get_json()["data"]["access_token"]

    # User B attempts to view User A's analysis
    forbidden_view = client.get(f"/api/analyses/{analysis_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert forbidden_view.status_code == 403

    # User B attempts to download User A's PDF
    forbidden_download = client.get(f"/api/analyses/{analysis_id}/report", headers={"Authorization": f"Bearer {token_b}"})
    assert forbidden_download.status_code == 403

    # User B attempts to delete User A's analysis
    forbidden_delete = client.delete(f"/api/analyses/{analysis_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert forbidden_delete.status_code == 403

def test_delete_analysis_owned_by_user(client):
    """Test that a user can delete their own analysis session."""
    reg = client.post("/api/auth/register", json={
        "full_name": "User Gamma",
        "email": "gamma@example.com",
        "password": "Password123!"
    })
    token = reg.get_json()["data"]["access_token"]

    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Gamma Resume - Python.")
    pdf_bytes = doc.tobytes()
    doc.close()

    res = client.post(
        "/api/analyses",
        data={"file": (io.BytesIO(pdf_bytes), "gamma.pdf"), "job_role_id": "1"},
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data"
    )
    analysis_id = res.get_json()["data"]["id"]

    # Delete
    del_res = client.delete(f"/api/analyses/{analysis_id}", headers={"Authorization": f"Bearer {token}"})
    assert del_res.status_code == 200

    # Ensure it's deleted
    get_res = client.get(f"/api/analyses/{analysis_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_res.status_code == 404

