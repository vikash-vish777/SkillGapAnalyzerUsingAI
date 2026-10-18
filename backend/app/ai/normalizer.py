from app.models.skill import Skill

class SkillNormalizer:
    """Resolves extracted skill items against canonical records stored in the database."""

    @staticmethod
    def normalize_extracted_skills(extracted_skills: dict[str, dict]) -> list[dict]:
        """Maps extracted skill dictionaries to canonical database entities.
        
        Args:
            extracted_skills (dict): Result from SkillExtractor.extract_skills()
            
        Returns:
            list[dict]: List of normalized skill dictionaries containing skill_id, name,
                        category, evidence snippet, and confidence score.
        """
        if not extracted_skills:
            return []

        normalized_results = []

        # Fetch canonical skills in batch to minimize DB roundtrips
        canonical_names = list(extracted_skills.keys())
        db_skills = Skill.query.filter(Skill.name.in_(canonical_names)).all()
        db_skill_map = {s.name: s for s in db_skills}

        for canonical_name, data in extracted_skills.items():
            db_skill = db_skill_map.get(canonical_name)
            
            skill_id = db_skill.id if db_skill else None
            category = db_skill.category if db_skill else data.get("category", "General")

            normalized_results.append({
                "skill_id": skill_id,
                "name": canonical_name,
                "category": category,
                "evidence": data.get("evidence", ""),
                "confidence_score": data.get("confidence", 1.0),
            })

        return normalized_results

