import io
from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.extensions import db, limiter
from app.models.job_role import JobRole
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import Analysis
from app.models.analysis_skill import AnalysisSkill
from app.models.recommendation import Recommendation
from app.models.skill import Skill
from app.services.document_service import DocumentService
from app.ai.preprocessor import TextPreprocessor
from app.ai.extractor import SkillExtractor
from app.ai.normalizer import SkillNormalizer
from app.services.matching_engine import SkillMatchingEngine
from app.services.recommendation_service import RecommendationService
from app.services.career_advisor import CareerAdvisorService
from app.ai.semantic_matcher import SemanticMatcher
from app.services.report_service import ReportService

analyses_bp = Blueprint("analyses", __name__)
extractor = SkillExtractor()

@analyses_bp.route("/analyses", methods=["POST"])
@limiter.limit("10 per minute")
def analyze_skill_gap():
    """Uploads a resume, extracts skills, compares against a target job role, and persists analysis."""
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

    analysis_id = None
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except Exception as exc:
        current_app.logger.info(f"JWT verification skipped or token expired: {exc}")
        user_id = None

    # 11. Relational Persistence (When User is Authenticated)
    if user_id:
        try:
            uid = int(user_id)
            user = db.session.get(User, uid)
            if user:
                # Create Resume record
                resume = Resume(
                    user_id=uid,
                    original_filename=file_storage.filename,
                    file_type=file_type,
                    processing_status="completed",
                )
                db.session.add(resume)
                db.session.flush()

                # Create Analysis record
                analysis_record = Analysis(
                    user_id=uid,
                    resume_id=resume.id,
                    job_role_id=role.id,
                    match_percentage=match_result["match_percentage"],
                    weighted_match_percentage=match_result["weighted_match_percentage"],
                    algorithm_version=match_result["algorithm_version"],
                )
                db.session.add(analysis_record)
                db.session.flush()
                analysis_id = analysis_record.id

                # Save Analysis Skills
                for s in match_result["matched_skills"]:
                    if s.get("skill_id"):
                        db.session.add(AnalysisSkill(
                            analysis_id=analysis_record.id,
                            skill_id=s["skill_id"],
                            match_status="matched",
                            importance_weight=s.get("importance_weight", 1.0),
                            evidence=s.get("evidence"),
                            confidence_score=s.get("confidence_score", 1.0),
                        ))

                for s in match_result["missing_skills"]:
                    if s.get("skill_id"):
                        db.session.add(AnalysisSkill(
                            analysis_id=analysis_record.id,
                            skill_id=s["skill_id"],
                            match_status="missing",
                            importance_weight=s.get("importance_weight", 1.0),
                        ))

                for s in match_result["additional_skills"]:
                    if s.get("skill_id"):
                        db.session.add(AnalysisSkill(
                            analysis_id=analysis_record.id,
                            skill_id=s["skill_id"],
                            match_status="additional",
                            evidence=s.get("evidence"),
                        ))

                # Save Recommendations
                for r in recommendations:
                    if r.get("skill_id"):
                        rec_text = f"{r['reason']} Topics: {', '.join(r.get('recommended_topics', []))}. Exercise: {r.get('practice_exercise')}"
                        db.session.add(Recommendation(
                            analysis_id=analysis_record.id,
                            skill_id=r["skill_id"],
                            priority=r["priority"],
                            recommendation_text=rec_text,
                        ))

                db.session.commit()
            else:
                current_app.logger.info(f"User ID {uid} does not exist in DB; skipping persistence.")
        except Exception as exc:
            db.session.rollback()
            current_app.logger.warning(f"Analysis persistence failed: {str(exc)}")

    response_data = {
        "id": analysis_id,
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
        "missing_skills": match_result["missing_skills"],
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

@analyses_bp.route("/analyses", methods=["GET"])
@jwt_required()
def get_user_analyses():
    """Retrieves all past analyses created by the authenticated user."""
    user_id = int(get_jwt_identity())
    analyses = (
        Analysis.query.filter_by(user_id=user_id)
        .order_by(Analysis.created_at.desc())
        .all()
    )

    data = [a.to_dict(include_details=False) for a in analyses]
    return jsonify({
        "success": True,
        "message": f"Retrieved {len(data)} past analyses.",
        "data": data,
        "errors": None,
    }), 200

@analyses_bp.route("/analyses/<int:analysis_id>", methods=["GET"])
@jwt_required()
def get_analysis_detail(analysis_id: int):
    """Retrieves full details of a specific past analysis with ownership verification."""
    user_id = int(get_jwt_identity())
    analysis = db.session.get(Analysis, analysis_id)

    if not analysis:
        return jsonify({
            "success": False,
            "message": f"Analysis with ID {analysis_id} not found.",
            "data": None,
            "errors": None,
        }), 404

    # Strict User Record Isolation Check
    if analysis.user_id != user_id:
        return jsonify({
            "success": False,
            "message": "Access denied: You do not have permission to view this analysis.",
            "data": None,
            "errors": None,
        }), 403

    return jsonify({
        "success": True,
        "message": "Analysis details retrieved successfully.",
        "data": analysis.to_dict(include_details=True),
        "errors": None,
    }), 200

@analyses_bp.route("/analyses/<int:analysis_id>", methods=["DELETE"])
@jwt_required()
def delete_analysis(analysis_id: int):
    """Deletes an analysis session owned by the authenticated user."""
    user_id = int(get_jwt_identity())
    analysis = db.session.get(Analysis, analysis_id)

    if not analysis:
        return jsonify({
            "success": False,
            "message": f"Analysis with ID {analysis_id} not found.",
            "data": None,
            "errors": None,
        }), 404

    if analysis.user_id != user_id:
        return jsonify({
            "success": False,
            "message": "Access denied: You cannot delete another user's analysis.",
            "data": None,
            "errors": None,
        }), 403

    db.session.delete(analysis)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Analysis #{analysis_id} deleted successfully.",
        "data": None,
        "errors": None,
    }), 200

@analyses_bp.route("/analyses/<int:analysis_id>/report", methods=["GET"])
@jwt_required()
def download_pdf_report(analysis_id: int):
    """Generates and streams a downloadable PDF report for an analysis."""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    analysis = db.session.get(Analysis, analysis_id)

    if not analysis:
        return jsonify({
            "success": False,
            "message": f"Analysis with ID {analysis_id} not found.",
            "data": None,
            "errors": None,
        }), 404

    # Strict User Record Isolation Check
    if analysis.user_id != user_id:
        return jsonify({
            "success": False,
            "message": "Access denied: You can only download reports for your own analyses.",
            "data": None,
            "errors": None,
        }), 403

    candidate_name = user.full_name if user else "Candidate"
    pdf_bytes = ReportService.generate_pdf_report(analysis, candidate_name)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"skill-gap-report-{analysis_id}.pdf",
    )
