import io
import pytest
import pymupdf
import docx
from werkzeug.datastructures import FileStorage
from app import create_app
from app.services.document_service import DocumentService
from app.ai.preprocessor import TextPreprocessor
from app.errors.exceptions import (
    UnsupportedFileTypeError,
    FileTooLargeError,
    EmptyDocumentError,
)

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client

def create_sample_pdf_bytes(text_content: str) -> bytes:
    """Helper to create a valid in-memory PDF with text content."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), text_content)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def create_sample_docx_bytes(paragraphs: list[str]) -> bytes:
    """Helper to create a valid in-memory DOCX file."""
    doc = docx.Document()
    for p in paragraphs:
        doc.add_paragraph(p)
    file_stream = io.BytesIO()
    doc.save(file_stream)
    return file_stream.getvalue()

def test_extract_text_from_valid_pdf():
    """Test extracting text from a well-formed PDF resume."""
    resume_text = "Jane Doe\nFull Stack Developer\nSkills: Python, React.js, Docker, SQL, Git."
    pdf_bytes = create_sample_pdf_bytes(resume_text)

    extracted = DocumentService.extract_text_from_pdf(pdf_bytes)
    assert "Jane Doe" in extracted
    assert "Full Stack Developer" in extracted
    assert "React.js" in extracted

def test_extract_text_from_valid_docx():
    """Test extracting text from a well-formed DOCX resume."""
    paragraphs = [
        "John Smith",
        "Data Scientist",
        "Expertise in Machine Learning, Pandas, scikit-learn, and Deep Learning."
    ]
    docx_bytes = create_sample_docx_bytes(paragraphs)

    extracted = DocumentService.extract_text_from_docx(docx_bytes)
    assert "John Smith" in extracted
    assert "Machine Learning" in extracted
    assert "scikit-learn" in extracted

def test_reject_spoofed_file_extension():
    """Test that a plain text file renamed to .pdf fails magic byte validation."""
    fake_pdf = FileStorage(
        stream=io.BytesIO(b"Hello world, I am just a plain text file renamed to resume.pdf"),
        filename="resume.pdf",
        content_type="application/pdf"
    )
    with pytest.raises(UnsupportedFileTypeError) as exc_info:
        DocumentService.validate_and_read(fake_pdf)
    assert "standard PDF specification" in str(exc_info.value)

def test_reject_executable_content():
    """Test that an executable file with PE header is blocked as a security violation."""
    fake_exe = FileStorage(
        stream=io.BytesIO(b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff"),
        filename="malicious_resume.pdf",
        content_type="application/pdf"
    )
    with pytest.raises(UnsupportedFileTypeError) as exc_info:
        DocumentService.validate_and_read(fake_exe)
    assert "Executable content detected" in str(exc_info.value)

def test_reject_oversized_file():
    """Test that files exceeding 5MB are rejected."""
    six_mb_stream = io.BytesIO(b"%PDF-" + b"0" * (6 * 1024 * 1024))
    large_file = FileStorage(
        stream=six_mb_stream,
        filename="giant_resume.pdf",
        content_type="application/pdf"
    )
    with pytest.raises(FileTooLargeError) as exc_info:
        DocumentService.validate_and_read(large_file)
    assert "exceeds maximum limit" in str(exc_info.value)

def test_reject_empty_document():
    """Test that an empty 0-byte file is rejected."""
    empty_file = FileStorage(
        stream=io.BytesIO(b""),
        filename="empty.pdf",
        content_type="application/pdf"
    )
    with pytest.raises(EmptyDocumentError):
        DocumentService.validate_and_read(empty_file)

def test_text_preprocessor_preserves_special_tech_terms():
    """Test that clean_text standardizes formatting while preserving C++, C#, .NET, Node.js."""
    raw = "Skills:  • C++ \t and C#\n• .NET Framework\n• Node.js & React.js\n• CI/CD Pipelines"
    cleaned = TextPreprocessor.clean_text(raw)

    assert "C++" in cleaned
    assert "C#" in cleaned
    assert ".NET" in cleaned
    assert "Node.js" in cleaned
    assert "React.js" in cleaned
    assert "CI/CD" in cleaned
    assert "\t" not in cleaned

def test_resume_upload_api_endpoint(client):
    """Test POST /api/resumes/upload with a valid PDF file."""
    pdf_bytes = create_sample_pdf_bytes("Alex Rivera\nSoftware Engineer\nExperience: Python, Flask, MySQL, Docker.")
    data = {
        "file": (io.BytesIO(pdf_bytes), "alex_resume.pdf")
    }

    response = client.post(
        "/api/resumes/upload",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    res_json = response.get_json()
    assert res_json["success"] is True
    assert res_json["data"]["filename"] == "alex_resume.pdf"
    assert res_json["data"]["file_type"] == "pdf"
    assert "Alex Rivera" in res_json["data"]["extracted_text"]
    assert res_json["data"]["word_count"] > 0

def test_resume_upload_missing_file_part(client):
    """Test POST /api/resumes/upload with missing file part returns 400."""
    response = client.post("/api/resumes/upload", data={}, content_type="multipart/form-data")
    assert response.status_code == 400
    res_json = response.get_json()
    assert res_json["success"] is False
    assert "No file part" in res_json["message"]

