from datetime import datetime, timezone
from app.extensions import db

class Analysis(db.Model):
    """Historical record of an executed skill gap analysis session."""
    __tablename__ = "analyses"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True)
    job_role_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("job_roles.id", ondelete="RESTRICT"), nullable=False, index=True)
    match_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    weighted_match_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    analysis_status = db.Column(
        db.Enum("completed", "failed", "archived", name="analysis_status_enum"),
        default="completed",
        nullable=False,
    )
    algorithm_version = db.Column(db.String(20), default="v1.0", nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    # Relationships
    user = db.relationship("User", back_populates="analyses")
    resume = db.relationship("Resume", back_populates="analyses")
    job_role = db.relationship("JobRole", back_populates="analyses")
    analysis_skills = db.relationship("AnalysisSkill", back_populates="analysis", cascade="all, delete-orphan", lazy="joined")
    recommendations = db.relationship("Recommendation", back_populates="analysis", cascade="all, delete-orphan", lazy="joined")

    def to_dict(self, include_details: bool = False) -> dict:
        """Serializes Analysis record to dictionary."""
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "resume_id": self.resume_id,
            "job_role_id": self.job_role_id,
            "job_role_title": self.job_role.title if self.job_role else None,
            "match_percentage": float(self.match_percentage) if self.match_percentage is not None else 0.0,
            "weighted_match_percentage": float(self.weighted_match_percentage) if self.weighted_match_percentage is not None else 0.0,
            "analysis_status": self.analysis_status,
            "algorithm_version": self.algorithm_version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_details:
            data["skills"] = [skill.to_dict() for skill in self.analysis_skills]
            data["recommendations"] = [rec.to_dict() for rec in self.recommendations]
        return data

    def __repr__(self) -> str:
        return f"<Analysis id={self.id} user_id={self.user_id} score={self.match_percentage}%>"
