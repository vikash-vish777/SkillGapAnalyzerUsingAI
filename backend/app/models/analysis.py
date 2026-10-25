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
            data["job_role"] = {
                "id": self.job_role.id if self.job_role else self.job_role_id,
                "title": self.job_role.title if self.job_role else "Target Role",
                "category": self.job_role.category if self.job_role else "Engineering",
            }

            matched = []
            missing = []
            essential = []
            preferred = []
            additional = []

            for s in self.analysis_skills:
                item = {
                    "skill_id": s.skill_id,
                    "name": s.skill.name if s.skill else f"Skill {s.skill_id}",
                    "category": s.skill.category if s.skill else "General",
                    "importance_weight": float(s.importance_weight) if s.importance_weight else 1.0,
                    "evidence": s.evidence or "",
                    "confidence_score": float(s.confidence_score) if s.confidence_score else 1.0,
                    "requirement_type": "essential" if s.importance_weight and s.importance_weight >= 1.2 else "preferred",
                }
                if s.match_status == "matched":
                    matched.append(item)
                elif s.match_status == "missing":
                    missing.append(item)
                    if item["requirement_type"] == "essential":
                        essential.append(item)
                    else:
                        preferred.append(item)
                elif s.match_status == "additional":
                    additional.append(item)

            data["matched_skills"] = matched
            data["missing_skills"] = missing
            data["essential_missing_skills"] = essential
            data["preferred_missing_skills"] = preferred
            data["additional_skills"] = additional
            data["matched_count"] = len(matched)
            data["missing_count"] = len(missing)
            data["total_required_count"] = len(matched) + len(missing)

            recs_list = []
            for rec in self.recommendations:
                skill_name = rec.skill.name if rec.skill else "Skill"
                resources = [r.to_dict() for r in (rec.skill.learning_resources if rec.skill else [])]
                recs_list.append({
                    "skill_name": skill_name,
                    "skill_id": rec.skill_id,
                    "priority": rec.priority,
                    "importance_level": "High (Essential Requirement)" if rec.priority == 1 else "Medium (Preferred Skill)",
                    "reason": rec.recommendation_text or f"Essential competency for {self.job_role.title if self.job_role else 'this role'}.",
                    "recommended_topics": [
                        f"Core principles and implementation of {skill_name}",
                        "Industry best practices and common design patterns",
                        "Building and deploying hands-on mini-projects",
                    ],
                    "practice_exercise": f"Implement a focused hands-on mini-project demonstrating practical application of {skill_name}.",
                    "estimated_learning_time": "1 to 2 weeks",
                    "resources": resources,
                    "completion_status": rec.completion_status or "pending",
                })
            data["recommendations"] = recs_list

            data["semantic_similarity"] = {
                "similarity_score": round(float(self.match_percentage) / 100.0 * 0.8, 2),
                "similarity_percentage": round(float(self.match_percentage) * 0.8, 1),
                "interpretation": (
                    "High Semantic Alignment"
                    if float(self.match_percentage) >= 70
                    else ("Moderate Semantic Alignment" if float(self.match_percentage) >= 40 else "Low Semantic Alignment")
                ),
                "shared_keywords": [s["name"].lower() for s in matched[:4]],
            }
            data["suggested_career_roles"] = []
        return data

    def __repr__(self) -> str:
        return f"<Analysis id={self.id} user_id={self.user_id} score={self.match_percentage}%>"
