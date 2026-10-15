class AppError(Exception):
    """Base exception for application errors."""
    status_code = 400

    def __init__(self, message: str, status_code: int = None, details: dict = None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.details = details or {}

class UnsupportedFileTypeError(AppError):
    """Raised when an uploaded file is not a supported format or signature fails."""
    status_code = 400

class FileTooLargeError(AppError):
    """Raised when an uploaded file exceeds the configured size limit."""
    status_code = 413

class EmptyDocumentError(AppError):
    """Raised when a document contains no readable text."""
    status_code = 400

class DocumentProcessingError(AppError):
    """Raised when parsing or text extraction from a document fails."""
    status_code = 422

