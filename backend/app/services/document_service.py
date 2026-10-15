import io
import zipfile
import pymupdf
import docx
from app.errors.exceptions import (
    UnsupportedFileTypeError,
    FileTooLargeError,
    EmptyDocumentError,
    DocumentProcessingError,
)

# Maximum file size allowed: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024

# Magic byte signatures
PDF_MAGIC_BYTES = b"%PDF-"
ZIP_MAGIC_BYTES = b"PK\x03\x04"
EXECUTABLE_MAGIC_BYTES = (b"MZ", b"\x7fELF")

class DocumentService:
    """Service for validating uploaded resumes and extracting text in-memory."""

    @staticmethod
    def validate_and_read(file_storage) -> tuple[bytes, str]:
        """Validates file presence, extension, size, and magic byte signatures.
        
        Returns:
            tuple[bytes, str]: Tuple of (raw_file_bytes, normalized_file_type)
        """
        if not file_storage or not getattr(file_storage, "filename", None):
            raise UnsupportedFileTypeError("No file was uploaded.")

        filename = file_storage.filename.strip()
        lower_name = filename.lower()

        # 1. Extension Check
        if lower_name.endswith(".pdf"):
            declared_type = "pdf"
        elif lower_name.endswith(".docx"):
            declared_type = "docx"
        else:
            raise UnsupportedFileTypeError(
                "Unsupported file format. Please upload a PDF (.pdf) or Word (.docx) document."
            )

        # 2. Read bytes into memory
        file_bytes = file_storage.read()
        if not file_bytes:
            raise EmptyDocumentError("The uploaded file is empty (0 bytes).")

        # 3. File Size Check
        if len(file_bytes) > MAX_FILE_SIZE:
            raise FileTooLargeError(
                f"File size ({len(file_bytes) / (1024 * 1024):.2f} MB) exceeds maximum limit of 5 MB."
            )

        # 4. Security Signature / Magic Byte Checks
        # Reject executable files disguised with doc extensions
        if any(file_bytes.startswith(sig) for sig in EXECUTABLE_MAGIC_BYTES):
            raise UnsupportedFileTypeError("Security violation: Executable content detected in uploaded file.")

        if declared_type == "pdf":
            if not file_bytes.startswith(PDF_MAGIC_BYTES):
                raise UnsupportedFileTypeError(
                    "Invalid PDF file. The file content does not match the standard PDF specification."
                )
        elif declared_type == "docx":
            if not file_bytes.startswith(ZIP_MAGIC_BYTES):
                raise UnsupportedFileTypeError(
                    "Invalid DOCX file. The file content does not match the standard DOCX specification."
                )
            # Verify internal docx package structure
            try:
                with zipfile.ZipFile(io.BytesIO(file_bytes), "r") as zf:
                    namelist = zf.namelist()
                    if "word/document.xml" not in namelist:
                        raise UnsupportedFileTypeError("Invalid Word document structure. Missing document.xml.")
            except zipfile.BadZipFile:
                raise UnsupportedFileTypeError("Corrupt or invalid DOCX archive.")

        return file_bytes, declared_type

    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extracts text streams from PDF bytes using PyMuPDF."""
        try:
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        except Exception as exc:
            raise DocumentProcessingError(f"Failed to open PDF document: {str(exc)}")

        if doc.is_encrypted:
            doc.close()
            raise DocumentProcessingError("Encrypted or password-protected PDFs are not supported.")

        extracted_pages = []
        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text("text")
                if text:
                    extracted_pages.append(text.strip())
        except Exception as exc:
            raise DocumentProcessingError(f"Error reading PDF page contents: {str(exc)}")
        finally:
            doc.close()

        full_text = "\n\n".join(extracted_pages).strip()
        if not full_text or len(full_text) < 15:
            raise EmptyDocumentError(
                "Document contains no extractable text. If this is a scanned document, please use an editable or text-based resume."
            )

        return full_text

    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        """Extracts text from DOCX bytes using python-docx."""
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
        except Exception as exc:
            raise DocumentProcessingError(f"Failed to parse DOCX document: {str(exc)}")

        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        # Extract text from tables if any
        table_lines = []
        for table in doc.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    table_lines.append(" | ".join(row_cells))

        full_text = "\n".join(paragraphs + table_lines).strip()
        if not full_text or len(full_text) < 15:
            raise EmptyDocumentError("The DOCX document contains no extractable text content.")

        return full_text

    @classmethod
    def extract_text(cls, file_bytes: bytes, file_type: str) -> str:
        """Dispatches extraction to appropriate parser based on validated file type."""
        if file_type == "pdf":
            return cls.extract_text_from_pdf(file_bytes)
        elif file_type == "docx":
            return cls.extract_text_from_docx(file_bytes)
        else:
            raise UnsupportedFileTypeError(f"Cannot extract text from unsupported type: {file_type}")

