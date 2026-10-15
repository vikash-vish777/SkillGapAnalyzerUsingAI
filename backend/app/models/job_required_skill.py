from datetime import datetime, timezone
from app.extensions import db

class JobRequiredSkill(db.Model):
    """Associative model defining required skills for a given job role."""
    __tablename__ = "job_required_skills"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True, autoincrement=True)
    job_role_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("job_roles.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    importance_weight = db.Column(db.Numeric(3, 2), default=1.00, nullable=False)
    requirement_type = db.Column(
        db.Enum("essential", "preferred", name="requirement_type_enum"),
        default="essential",
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    job_role = db.relationship("JobRole", back_populates="required_skills")
    skill = db.relationship("Skill", back_populates="job_requirements", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("job_role_id", "skill_id", name="uq_job_role_skill"),
    )

    def to_dict(self) -> dict:
        """Serializes JobRequiredSkill to dictionary."""
        return {
            "id": self.id,
            "job_role_id": self.job_role_id,
            "skill_id": self.skill_id,
            "skill_name": self.skill.name if self.skill else None,
            "category": self.skill.category if self.skill else None,
            "importance_weight": float(self.importance_weight) if self.importance_weight is not None else 1.0,
            "requirement_type": self.requirement_type,
        }

    def __repr__(self) -> str:
        return f"<JobRequiredSkill role_id={self.job_role_id} skill_id={self.skill_id} type='{self.requirement_type}'>"
