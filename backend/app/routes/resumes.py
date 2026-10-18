from flask import Blueprint, request, jsonify
from app.extensions import limiter
from app.services.document_service import DocumentService
from app.ai.preprocessor import TextPreprocessor

resumes_bp = Blueprint("resumes", __name__)

@resumes_bp.route("/resumes/upload", methods=["POST"])
@limiter.limit("10 per minute")
def upload_and_extract_resume():
    """Uploads a PDF or DOCX resume, validates its signature, and extracts clean text."""
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file part in the request. Please provide a file with key 'file'.",
            "data": None,
            "errors": None
        }), 400

    file_storage = request.files["file"]

    # 1. Validate signature, format, and size in-memory
    file_bytes, file_type = DocumentService.validate_and_read(file_storage)

    # 2. Extract text stream
    raw_text = DocumentService.extract_text(file_bytes, file_type)

    # 3. Clean and normalize text
    cleaned_text = TextPreprocessor.clean_text(raw_text)

    # Compute text metadata
    words = cleaned_text.split()
    preview = cleaned_text[:300] + ("..." if len(cleaned_text) > 300 else "")

    return jsonify({
        "success": True,
        "message": f"Resume '{file_storage.filename}' processed successfully.",
        "data": {
            "filename": file_storage.filename,
            "file_type": file_type,
            "character_count": len(cleaned_text),
            "word_count": len(words),
            "preview_snippet": preview,
            "extracted_text": cleaned_text
        },
        "errors": None
    }), 200

