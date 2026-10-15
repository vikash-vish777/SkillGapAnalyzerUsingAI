from datetime import datetime, timezone
from app.extensions import db

class JobRole(db.Model):
    """Industry job role definition with required competencies."""
    __tablename__ = "job_roles"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    required_skills = db.relationship(
        "JobRequiredSkill",
        back_populates="job_role",
        cascade="all, delete-orphan",
        lazy="joined"
    )
    analyses = db.relationship("Analysis", back_populates="job_role", lazy="dynamic")

    def to_dict(self, include_skills: bool = False) -> dict:
        """Serializes JobRole to dictionary."""
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_skills:
            data["required_skills"] = [req.to_dict() for req in self.required_skills]
        return data

    def __repr__(self) -> str:
        return f"<JobRole id={self.id} title='{self.title}'>"
