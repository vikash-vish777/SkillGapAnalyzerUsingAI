from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.job_role import JobRole
from app.services.document_service import DocumentService
from app.ai.preprocessor import TextPreprocessor
from app.ai.extractor import SkillExtractor
from app.ai.normalizer import SkillNormalizer
from app.services.matching_engine import SkillMatchingEngine
from app.services.recommendation_service import RecommendationService
from app.services.career_advisor import CareerAdvisorService
from app.ai.semantic_matcher import SemanticMatcher

analyses_bp = Blueprint("analyses", __name__)
extractor = SkillExtractor()

@analyses_bp.route("/analyses", methods=["POST"])
def analyze_skill_gap():
    """Uploads a resume, extracts skills, compares against a target job role, and calculates skill gaps."""
    # 1. Validate file presence
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "Resume file is required. Please provide a file with key 'file'.",
            "data": None,
            "errors": None,
        }), 400

    file_storage = request.files["file"]

    # 2. Validate job_role_id
    job_role_id = request.form.get("job_role_id")
    if not job_role_id:
        return jsonify({
            "success": False,
            "message": "Field 'job_role_id' is required.",
            "data": None,
            "errors": None,
        }), 400

    try:
        job_role_id = int(job_role_id)
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Field 'job_role_id' must be an integer.",
            "data": None,
            "errors": None,
        }), 400

    # 3. Retrieve target job role from database
    role = db.session.get(JobRole, job_role_id)
    if not role:
        return jsonify({
            "success": False,
            "message": f"Job role with ID {job_role_id} not found.",
            "data": None,
            "errors": None,
        }), 404

    # 4. Validate and extract text from resume
    file_bytes, file_type = DocumentService.validate_and_read(file_storage)
    raw_text = DocumentService.extract_text(file_bytes, file_type)
    cleaned_text = TextPreprocessor.clean_text(raw_text)

    # 5. Extract and normalize candidate skills
    raw_extracted = extractor.extract_skills(cleaned_text)
    candidate_skills = SkillNormalizer.normalize_extracted_skills(raw_extracted)

    # 6. Retrieve job requirements
    role_requirements = [req.to_dict() for req in role.required_skills]

    # Optional: Analyze custom job description if supplied by candidate
    custom_jd = request.form.get("custom_job_description")
    if custom_jd and custom_jd.strip():
        custom_jd_cleaned = TextPreprocessor.clean_text(custom_jd)
        custom_skills = extractor.extract_skills(custom_jd_cleaned)
        existing_req_names = {r["skill_name"].lower() for r in role_requirements}
        for sname, sinfo in custom_skills.items():
            if sname.lower() not in existing_req_names:
                role_requirements.append({
                    "skill_name": sname,
                    "category": sinfo.get("category", "General"),
                    "importance_weight": 1.2,
                    "requirement_type": "essential",
                })

    # 7. Execute Deterministic Skill Matching & Gap Scoring
    match_result = SkillMatchingEngine.compare_skills(candidate_skills, role_requirements)

    # 8. Generate Actionable Learning Recommendations
    recommendations = RecommendationService.generate_recommendations(match_result["missing_skills"])

    # 9. Discover Alternative Career Paths
    career_suggestions = CareerAdvisorService.recommend_alternative_roles(
        candidate_skills,
        current_job_role_id=role.id,
        min_overlap_threshold=25.0,
        limit=3,
    )

    # 10. Semantic Similarity Analysis (TF-IDF + Cosine)
    jd_reference_text = (
        custom_jd if (custom_jd and custom_jd.strip())
        else f"{role.title}. {role.description or ''}. Skills required: {', '.join([r['skill_name'] for r in role_requirements])}"
    )
    semantic_report = SemanticMatcher.compute_similarity(cleaned_text, jd_reference_text)

    response_data = {
        "job_role": {
            "id": role.id,
            "title": role.title,
            "category": role.category,
        },
        "match_percentage": match_result["match_percentage"],
        "weighted_match_percentage": match_result["weighted_match_percentage"],
        "total_required_count": match_result["total_required_count"],
        "matched_count": match_result["matched_count"],
        "missing_count": match_result["missing_count"],
        "matched_skills": match_result["matched_skills"],
        "essential_missing_skills": match_result["essential_missing_skills"],
        "preferred_missing_skills": match_result["preferred_missing_skills"],
        "additional_skills": match_result["additional_skills"],
        "recommendations": recommendations,
        "suggested_career_roles": career_suggestions,
        "semantic_similarity": semantic_report,
        "algorithm_version": match_result["algorithm_version"],
    }

    return jsonify({
        "success": True,
        "message": f"Skill gap analysis against '{role.title}' completed successfully.",
        "data": response_data,
        "errors": None,
    }), 200
