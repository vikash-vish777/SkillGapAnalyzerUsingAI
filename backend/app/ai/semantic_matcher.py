from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticMatcher:
    """Computes TF-IDF vector representations and Cosine Similarity between resumes and job descriptions."""

    @classmethod
    def compute_similarity(cls, resume_text: str, job_description_text: str) -> dict:
        """Calculates semantic similarity between resume content and job description.
        
        Args:
            resume_text (str): Cleaned resume text.
            job_description_text (str): Target job role or custom job description text.
            
        Returns:
            dict: Structured similarity report containing cosine score, percentage,
                  interpretation, and top overlapping terms.
        """
        if not resume_text or not job_description_text:
            return {
                "similarity_score": 0.0,
                "similarity_percentage": 0.0,
                "interpretation": "Insufficient text for semantic comparison",
                "shared_keywords": [],
            }

        documents = [resume_text, job_description_text]

        try:
            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 1),
                max_features=500,
                token_pattern=r"(?u)\b\w[\w\+\#\.\-]+\b"  # Retain C++, C#, .NET
            )
            tfidf_matrix = vectorizer.fit_transform(documents)

            # Cosine similarity between resume (row 0) and JD (row 1)
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            raw_score = float(similarity_matrix[0][0])
            score = round(max(0.0, min(1.0, raw_score)), 4)
            percentage = round(score * 100.0, 2)

            # Identify top shared features (terms with non-zero weight in both documents)
            feature_names = vectorizer.get_feature_names_out()
            resume_vector = tfidf_matrix[0].toarray()[0]
            jd_vector = tfidf_matrix[1].toarray()[0]

            shared_terms = []
            for idx, term in enumerate(feature_names):
                if resume_vector[idx] > 0 and jd_vector[idx] > 0:
                    combined_weight = float(resume_vector[idx] * jd_vector[idx])
                    shared_terms.append((term, combined_weight))

            shared_terms.sort(key=lambda x: x[1], reverse=True)
            top_shared = [term for term, _ in shared_terms[:8]]

            if percentage >= 35.0:
                interpretation = "High Semantic Alignment"
            elif percentage >= 15.0:
                interpretation = "Moderate Semantic Alignment"
            elif percentage >= 5.0:
                interpretation = "Low Semantic Alignment"
            else:
                interpretation = "Minimal Semantic Alignment"

            return {
                "similarity_score": score,
                "similarity_percentage": percentage,
                "interpretation": interpretation,
                "shared_keywords": top_shared,
            }

        except Exception as exc:
            return {
                "similarity_score": 0.0,
                "similarity_percentage": 0.0,
                "interpretation": f"Error computing semantic similarity: {str(exc)}",
                "shared_keywords": [],
            }

