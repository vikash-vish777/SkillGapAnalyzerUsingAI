# Skill Gap Analyzer Using Artificial Intelligence (AI)

An enterprise-ready, AI-driven web application that bridges the gap between candidates' existing skills and market job requirements. It ingests resumes in PDF and DOCX formats, extracts and normalizes technical competencies using hybrid NLP pipelines, benchmarks candidates against industry roles, computes transparent match percentages, and generates personalized learning roadmaps.

---

## 1. Project Overview

- **Audience**: Students, fresh graduates, job seekers, and career changers.
- **Problem**: Candidates struggle to know why their resumes are filtered out and what specific skills they lack for their dream jobs.
- **Solution**: Automated parsing, skill extraction, deterministic and semantic gap analysis, transparent match calculation, and verified learning recommendations.

---

## 2. Technology Stack

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Bootstrap 5 + Modern Custom CSS
- **Routing**: React Router v6
- **HTTP Client**: Axios with JWT interceptors
- **Visualizations**: Chart.js / Recharts

### Backend & AI
- **Framework**: Python 3.13, Flask (Application Factory & Blueprints)
- **Database & ORM**: MySQL 8.0, Flask-SQLAlchemy, Flask-Migrate (Alembic)
- **Authentication**: Flask-JWT-Extended, Passlib / Bcrypt
- **NLP & Document Parsing**: spaCy, PyMuPDF (fitz), python-docx, scikit-learn
- **Validation**: Marshmallow, python-magic / pure-python MIME verification

---

## 3. Architecture & Data Flow

```
User (Browser)
    │ (Uploads PDF/DOCX + Selects Job Role)
    ▼
React SPA (Frontend)
    │ (REST API via Axios with JWT)
    ▼
Flask API Gateway
    ├── Auth & Rate Limiting Middleware
    ├── File Validation & Security Inspector
    ├── Document Parser (PyMuPDF / python-docx)
    ├── NLP Skill Extractor & Canonical Normalizer
    ├── Skill-Matching Engine (Basic & Weighted Scoring)
    ├── Recommendation Generator
    └── MySQL 8.0 Database (Normalized 3NF)
```

For detailed specifications, see:
- [System Architecture](file:///d:/SkillGapAnalyzerUsingAI/docs/architecture.md)
- [Database Design & ERD](file:///d:/SkillGapAnalyzerUsingAI/docs/database-design.md)
- [REST API Documentation](file:///d:/SkillGapAnalyzerUsingAI/docs/api-documentation.md)
- [Testing Strategy](file:///d:/SkillGapAnalyzerUsingAI/docs/testing-strategy.md)

---

## 4. Development Roadmap

- [x] **Phase 1: Planning & Architecture** (Specs, ERD, API Contracts, Repo setup)
- [ ] **Phase 2: Environment Setup** (Backend venv, Flask skeleton, Frontend Vite skeleton)
- [ ] **Phase 3: Database & Backend Core** (SQLAlchemy models, migrations, seed data, health checks)
- [ ] **Phase 4: Resume Processing** (MIME validation, text extraction, NLP preprocessing)
- [ ] **Phase 5: Skill Analysis Engine** (Dictionary extractor, normalizer, gap analysis, scoring)
- [ ] **Phase 6: AI Enhancement & Recommendations** (Semantic similarity, career suggestions, roadmaps)
- [ ] **Phase 7: Frontend Application** (Responsive UI, dashboard, dropzone, analysis views)
- [ ] **Phase 8: Full-Stack Integration** (API wiring, state management, persistence, history)
- [ ] **Phase 9: Security & Automated Testing** (Pytest suite, user data isolation, error audits)
- [ ] **Phase 10: Deployment Preparation** (Vercel config, WSGI setup, Docker/cloud manifests)
- [ ] **Phase 11: Final Documentation & Demonstration** (Full guide, screenshots, demo walkthrough)
