import pymupdf
from app.models.analysis import Analysis

class ReportService:
    """Generates official downloadable PDF skill gap analysis reports."""

    @classmethod
    def generate_pdf_report(cls, analysis: Analysis, candidate_name: str = "Candidate") -> bytes:
        """Constructs a multi-page styled PDF report using PyMuPDF.
        
        Args:
            analysis (Analysis): Analysis SQLAlchemy model instance with relationships loaded.
            candidate_name (str): Full name of the candidate.
            
        Returns:
            bytes: Binary content of the generated PDF document.
        """
        doc = pymupdf.open()
        page = doc.new_page(width=595, height=842)  # Standard A4: 595 x 842 points
        
        # Color palette (RGB normalized 0.0 - 1.0)
        primary_color = (0.145, 0.388, 0.921)   # #2563eb
        dark_color = (0.118, 0.161, 0.231)      # #1e293b
        muted_color = (0.392, 0.455, 0.545)     # #64748b
        success_color = (0.063, 0.725, 0.506)   # #10b981
        danger_color = (0.937, 0.267, 0.267)    # #ef4444

        y = 50

        # Header Title
        page.insert_text(
            (50, y),
            "SKILL GAP ANALYZER USING AI",
            fontsize=18,
            fontname="helv",
            color=primary_color,
        )
        y += 20
        page.insert_text(
            (50, y),
            "Official Candidate Competency & Learning Roadmap Report",
            fontsize=10,
            fontname="helv",
            color=muted_color,
        )
        y += 15

        # Horizontal Divider line
        page.draw_line((50, y), (545, y), color=primary_color, width=1.5)
        y += 25

        # Metadata Box
        page.draw_rect(pymupdf.Rect(50, y, 545, y + 65), color=None, fill=(0.96, 0.97, 0.98))
        meta_y = y + 18
        page.insert_text((65, meta_y), f"Candidate: {candidate_name}", fontsize=10, fontname="helv", color=dark_color)
        page.insert_text((300, meta_y), f"Analysis ID: #{analysis.id}", fontsize=10, fontname="helv", color=dark_color)
        meta_y += 18
        page.insert_text((65, meta_y), f"Target Role: {analysis.job_role.title}", fontsize=10, fontname="helv", color=dark_color)
        page.insert_text((300, meta_y), f"Category: {analysis.job_role.category}", fontsize=10, fontname="helv", color=dark_color)
        meta_y += 18
        date_str = analysis.created_at.strftime("%Y-%m-%d %H:%M UTC") if analysis.created_at else "N/A"
        page.insert_text((65, meta_y), f"Date Evaluated: {date_str}", fontsize=9, fontname="helv", color=muted_color)
        page.insert_text((300, meta_y), f"Algorithm: {analysis.algorithm_version}", fontsize=9, fontname="helv", color=muted_color)
        y += 85

        # Scores Section
        page.insert_text((50, y), "EXECUTIVE SCORECARD", fontsize=12, fontname="helv", color=primary_color)
        y += 20

        # Score cards rects
        page.draw_rect(pymupdf.Rect(50, y, 290, y + 55), color=(0.85, 0.88, 0.92), fill=(1, 1, 1), width=1)
        page.draw_rect(pymupdf.Rect(305, y, 545, y + 55), color=(0.85, 0.88, 0.92), fill=(1, 1, 1), width=1)

        page.insert_text((65, y + 20), "BASIC SKILL MATCH", fontsize=8, fontname="helv", color=muted_color)
        page.insert_text((65, y + 42), f"{float(analysis.match_percentage):.1f}%", fontsize=18, fontname="helv", color=primary_color)

        page.insert_text((320, y + 20), "WEIGHTED IMPORTANCE MATCH", fontsize=8, fontname="helv", color=muted_color)
        page.insert_text((320, y + 42), f"{float(analysis.weighted_match_percentage):.1f}%", fontsize=18, fontname="helv", color=success_color)
        y += 75

        # Scoring Methodology
        page.insert_text((50, y), "Scoring Methodology:", fontsize=9, fontname="helv", color=dark_color)
        y += 12
        page.insert_text(
            (50, y),
            "Basic Match % = (Matched Required Skills / Total Required Skills) * 100",
            fontsize=8,
            fontname="helv",
            color=muted_color,
        )
        y += 12
        page.insert_text(
            (50, y),
            "Weighted Match % = (Sum of Matched Weights / Sum of Total Required Weights) * 100",
            fontsize=8,
            fontname="helv",
            color=muted_color,
        )
        y += 25

        # Competency Breakdown
        page.insert_text((50, y), "SKILL COMPETENCY BREAKDOWN", fontsize=12, fontname="helv", color=primary_color)
        y += 20

        matched_skills = [s for s in analysis.analysis_skills if s.match_status == "matched"]
        missing_skills = [s for s in analysis.analysis_skills if s.match_status == "missing"]
        additional_skills = [s for s in analysis.analysis_skills if s.match_status == "additional"]

        # Matched Skills summary
        page.insert_text((50, y), f"Matched Skills ({len(matched_skills)}):", fontsize=9, fontname="helv", color=success_color)
        y += 14
        matched_str = ", ".join([s.skill.name for s in matched_skills]) if matched_skills else "None identified"
        page.insert_text((50, y), matched_str[:90], fontsize=8, fontname="helv", color=dark_color)
        y += 18

        # Missing Skills summary
        page.insert_text((50, y), f"Identified Skill Gaps ({len(missing_skills)}):", fontsize=9, fontname="helv", color=danger_color)
        y += 14
        missing_str = ", ".join([f"{s.skill.name} (wt: {s.importance_weight})" for s in missing_skills]) if missing_skills else "None - 100% matched!"
        page.insert_text((50, y), missing_str[:90], fontsize=8, fontname="helv", color=dark_color)
        y += 18

        # Additional Skills summary
        if additional_skills:
            page.insert_text((50, y), f"Additional Demonstrable Skills ({len(additional_skills)}):", fontsize=9, fontname="helv", color=muted_color)
            y += 14
            add_str = ", ".join([s.skill.name for s in additional_skills[:8]])
            page.insert_text((50, y), add_str[:90], fontsize=8, fontname="helv", color=dark_color)
            y += 25

        # Recommendations Section
        if analysis.recommendations:
            page.insert_text((50, y), "PRIORITIZED LEARNING ROADMAPS", fontsize=12, fontname="helv", color=primary_color)
            y += 20

            for rec in analysis.recommendations[:4]:
                priority_label = "Priority 1 - Essential" if rec.priority == 1 else "Priority 2 - Preferred"
                p_color = danger_color if rec.priority == 1 else muted_color
                
                page.insert_text((50, y), f"• {rec.skill.name} [{priority_label}]", fontsize=9, fontname="helv", color=p_color)
                y += 12
                # Wrap recommendation text
                rec_snippet = rec.recommendation_text[:110]
                page.insert_text((65, y), rec_snippet, fontsize=8, fontname="helv", color=dark_color)
                y += 18

        # Footer Disclaimer
        page.draw_line((50, 785), (545, 785), color=(0.8, 0.8, 0.8), width=0.5)
        page.insert_text(
            (50, 800),
            "Disclaimer: This report represents automated AI NLP skill extraction and deterministic scoring. It does not constitute a hiring guarantee.",
            fontsize=7,
            fontname="helv",
            color=muted_color,
        )

        pdf_bytes = doc.tobytes()
        doc.close()
        return pdf_bytes

