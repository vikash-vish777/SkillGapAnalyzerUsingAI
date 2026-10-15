from datetime import datetime, timezone
from app.extensions import db

class Recommendation(db.Model):
    """Actionable learning recommendation generated from an identified skill gap."""
    __tablename__ = "recommendations"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True, autoincrement=True)
    analysis_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("skills.id", ondelete="RESTRICT"), nullable=False, index=True)
    priority = db.Column(db.Integer, default=1, nullable=False)  # 1 = Essential, 2 = Preferred
    recommendation_text = db.Column(db.Text, nullable=False)
    completion_status = db.Column(
        db.Enum("pending", "in_progress", "completed", name="completion_status_enum"),
        default="pending",
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    analysis = db.relationship("Analysis", back_populates="recommendations")
    skill = db.relationship("Skill", back_populates="recommendations", lazy="joined")

    def to_dict(self) -> dict:
        """Serializes Recommendation entry to dictionary."""
        return {
            "id": self.id,
            "skill_id": self.skill_id,
            "skill_name": self.skill.name if self.skill else None,
            "priority": self.priority,
            "recommendation_text": self.recommendation_text,
            "completion_status": self.completion_status,
            "resources": [res.to_dict() for res in self.skill.learning_resources] if self.skill else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Recommendation id={self.id} analysis_id={self.analysis_id} skill_id={self.skill_id}>"
