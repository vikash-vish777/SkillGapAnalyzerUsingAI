from datetime import datetime, timezone
from app.extensions import db

class LearningResource(db.Model):
    """Verified curated learning resource linked to a canonical skill."""
    __tablename__ = "learning_resources"

    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True, autoincrement=True)
    skill_id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), db.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    resource_url = db.Column(db.String(500), nullable=False)
    resource_type = db.Column(
        db.Enum("documentation", "course", "tutorial", "book", "project", name="resource_type_enum"),
        nullable=False,
    )
    difficulty_level = db.Column(
        db.Enum("beginner", "intermediate", "advanced", name="difficulty_level_enum"),
        default="beginner",
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    skill = db.relationship("Skill", back_populates="learning_resources")

    def to_dict(self) -> dict:
        """Serializes LearningResource entry to dictionary."""
        return {
            "id": self.id,
            "skill_id": self.skill_id,
            "title": self.title,
            "description": self.description,
            "resource_url": self.resource_url,
            "resource_type": self.resource_type,
            "difficulty_level": self.difficulty_level,
        }

    def __repr__(self) -> str:
        return f"<LearningResource id={self.id} skill_id={self.skill_id} title='{self.title}'>"
