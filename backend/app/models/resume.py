from datetime import datetime, timezone
from app.extensions import db

class Resume(db.Model):
    """Uploaded resume audit metadata. Raw file streams are processed in-memory."""
    __tablename__ = "resumes"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    processing_status = db.Column(
        db.Enum("pending", "completed", "failed", name="resume_status_enum"),
        default="completed",
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="resumes")
    analyses = db.relationship("Analysis", back_populates="resume", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        """Serializes resume record to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "original_filename": self.original_filename,
            "file_type": self.file_type,
            "processing_status": self.processing_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Resume id={self.id} user_id={self.user_id} filename='{self.original_filename}'>"
