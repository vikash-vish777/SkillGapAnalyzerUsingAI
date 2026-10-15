from datetime import datetime, timezone
from app.extensions import db

class AnalysisSkill(db.Model):
    """Granular skill-level evaluation associated with a specific analysis session."""
    __tablename__ = "analysis_skills"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True, autoincrement=True)
    analysis_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("skills.id", ondelete="RESTRICT"), nullable=False, index=True)
    match_status = db.Column(
        db.Enum("matched", "missing", "additional", name="match_status_enum"),
        nullable=False,
        index=True,
    )
    importance_weight = db.Column(db.Numeric(3, 2), default=1.00, nullable=False)
    evidence = db.Column(db.Text, nullable=True)
    confidence_score = db.Column(db.Numeric(4, 3), default=1.000, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    analysis = db.relationship("Analysis", back_populates="analysis_skills")
    skill = db.relationship("Skill", back_populates="analysis_skills", lazy="joined")

    def to_dict(self) -> dict:
        """Serializes AnalysisSkill entry to dictionary."""
        return {
            "id": self.id,
            "skill_id": self.skill_id,
            "skill_name": self.skill.name if self.skill else None,
            "category": self.skill.category if self.skill else None,
            "match_status": self.match_status,
            "importance_weight": float(self.importance_weight) if self.importance_weight is not None else 1.0,
            "evidence": self.evidence,
            "confidence_score": float(self.confidence_score) if self.confidence_score is not None else 1.0,
        }

    def __repr__(self) -> str:
        return f"<AnalysisSkill analysis_id={self.analysis_id} skill_id={self.skill_id} status='{self.match_status}'>"
