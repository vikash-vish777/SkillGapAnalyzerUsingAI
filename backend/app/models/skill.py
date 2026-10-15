from datetime import datetime, timezone
from app.extensions import db

class Skill(db.Model):
    """Canonical skill dictionary item."""
    __tablename__ = "skills"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    normalized_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    job_requirements = db.relationship("JobRequiredSkill", back_populates="skill", cascade="all, delete-orphan")
    learning_resources = db.relationship("LearningResource", back_populates="skill", cascade="all, delete-orphan", lazy="joined")
    analysis_skills = db.relationship("AnalysisSkill", back_populates="skill")
    recommendations = db.relationship("Recommendation", back_populates="skill")

    def to_dict(self, include_resources: bool = False) -> dict:
        """Serializes Skill to dictionary."""
        data = {
            "id": self.id,
            "name": self.name,
            "normalized_name": self.normalized_name,
            "category": self.category,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_resources:
            data["learning_resources"] = [res.to_dict() for res in self.learning_resources]
        return data

    def __repr__(self) -> str:
        return f"<Skill id={self.id} name='{self.name}'>"
