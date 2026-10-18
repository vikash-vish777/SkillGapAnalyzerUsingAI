class SkillMatchingEngine:
    """Calculates deterministic match scores, identifies gaps, and categorizes competencies."""

    ALGORITHM_VERSION = "v1.0"

    @classmethod
    def compare_skills(
        cls,
        candidate_skills: list[dict],
        role_requirements: list[dict],
    ) -> dict:
        """Compares candidate skills against role requirements.
        
        Args:
            candidate_skills (list[dict]): Extracted skills from candidate's resume.
                Each dict has: name, skill_id, category, evidence, confidence_score
            role_requirements (list[dict]): Required skills for the target role.
                Each dict has: skill_name, skill_id, importance_weight, requirement_type
                
        Returns:
            dict: Structured matching report with scores and categorized skill lists.
        """
        # Map candidate skills by lower-cased canonical name for O(1) lookups
        candidate_map = {cs["name"].lower(): cs for cs in candidate_skills}

        matched_skills = []
        missing_skills = []
        essential_missing = []
        preferred_missing = []

        total_required_weight = 0.0
        matched_weight = 0.0

        matched_skill_names_lower = set()

        for req in role_requirements:
            skill_name = req["skill_name"]
            weight = float(req.get("importance_weight", 1.0))
            req_type = req.get("requirement_type", "essential")

            total_required_weight += weight
            name_lower = skill_name.lower()

            if name_lower in candidate_map:
                candidate_info = candidate_map[name_lower]
                matched_skill_names_lower.add(name_lower)
                matched_weight += weight

                matched_skills.append({
                    "skill_id": req.get("skill_id"),
                    "name": skill_name,
                    "category": req.get("category", candidate_info.get("category", "General")),
                    "requirement_type": req_type,
                    "importance_weight": weight,
                    "evidence": candidate_info.get("evidence", ""),
                    "confidence_score": candidate_info.get("confidence_score", 1.0),
                })
            else:
                missing_item = {
                    "skill_id": req.get("skill_id"),
                    "name": skill_name,
                    "category": req.get("category", "General"),
                    "requirement_type": req_type,
                    "importance_weight": weight,
                }
                missing_skills.append(missing_item)
                if req_type == "essential":
                    essential_missing.append(missing_item)
                else:
                    preferred_missing.append(missing_item)

        # Identify additional skills candidate possesses that were not required for this role
        additional_skills = [
            cs for cs in candidate_skills
            if cs["name"].lower() not in matched_skill_names_lower
        ]

        # Calculate scores
        total_required_count = len(role_requirements)
        matched_count = len(matched_skills)

        if total_required_count > 0:
            basic_match_percentage = round((matched_count / total_required_count) * 100.0, 2)
        else:
            basic_match_percentage = 100.0 if not candidate_skills else 0.0

        if total_required_weight > 0:
            weighted_match_percentage = round((matched_weight / total_required_weight) * 100.0, 2)
        else:
            weighted_match_percentage = basic_match_percentage

        return {
            "algorithm_version": cls.ALGORITHM_VERSION,
            "total_required_count": total_required_count,
            "matched_count": matched_count,
            "missing_count": len(missing_skills),
            "match_percentage": basic_match_percentage,
            "weighted_match_percentage": weighted_match_percentage,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "essential_missing_skills": essential_missing,
            "preferred_missing_skills": preferred_missing,
            "additional_skills": additional_skills,
        }

