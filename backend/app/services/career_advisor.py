from app.models.job_role import JobRole

class CareerAdvisorService:
    """Discovers alternative career paths where the candidate has high skill overlap."""

    @classmethod
    def recommend_alternative_roles(
        cls,
        candidate_skills: list[dict],
        current_job_role_id: int,
        min_overlap_threshold: float = 30.0,
        limit: int = 3,
    ) -> list[dict]:
        """Analyzes all other available job roles and identifies those with high skill affinity.
        
        Args:
            candidate_skills (list[dict]): Extracted skills from candidate.
            current_job_role_id (int): ID of role currently being analyzed (excluded from suggestions).
            min_overlap_threshold (float): Minimum match percentage required to suggest a role (default 30%).
            limit (int): Maximum number of alternate career paths to suggest.
            
        Returns:
            list[dict]: Ranked list of alternate career role recommendations with rationales.
        """
        if not candidate_skills:
            return []

        candidate_skill_names_lower = {cs["name"].lower() for cs in candidate_skills}

        # Query all roles from database except current target role
        all_roles = JobRole.query.filter(JobRole.id != current_job_role_id).all()
        career_suggestions = []

        for role in all_roles:
            requirements = role.required_skills
            if not requirements:
                continue

            matched_in_role = []
            missing_in_role = []

            for req in requirements:
                skill = req.skill
                if not skill:
                    continue

                if skill.name.lower() in candidate_skill_names_lower:
                    matched_in_role.append(skill.name)
                else:
                    missing_in_role.append(skill.name)

            total_reqs = len(requirements)
            match_percentage = round((len(matched_in_role) / total_reqs) * 100.0, 2)

            if match_percentage >= min_overlap_threshold:
                # Construct realistic, transparent explanation
                overlap_sample = ", ".join(matched_in_role[:3])
                if len(matched_in_role) > 3:
                    overlap_sample += f", and {len(matched_in_role) - 3} other skills"

                if missing_in_role:
                    reason = (
                        f"Strong competency overlap ({match_percentage}%) for '{role.title}' based on your experience with {overlap_sample}. "
                        f"Acquiring {', '.join(missing_in_role[:2])} would position you well for this path."
                    )
                else:
                    reason = (
                        f"Exceptional 100% competency match for '{role.title}' based on your experience with {overlap_sample}."
                    )

                career_suggestions.append({
                    "role_id": role.id,
                    "title": role.title,
                    "category": role.category,
                    "match_percentage": match_percentage,
                    "matched_count": len(matched_in_role),
                    "total_required": total_reqs,
                    "matched_skills": matched_in_role,
                    "transition_skills_needed": missing_in_role,
                    "recommendation_reason": reason,
                    "disclaimer": "Skill overlap alignment only; does not guarantee employment or hiring qualification.",
                })

        # Rank suggestions: highest match percentage first
        career_suggestions.sort(key=lambda s: s["match_percentage"], reverse=True)
        return career_suggestions[:limit]

