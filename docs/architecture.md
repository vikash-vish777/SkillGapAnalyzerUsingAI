# System Architecture: Skill Gap Analyzer Using Artificial Intelligence (AI)

## 1. High-Level System Overview

The **Skill Gap Analyzer Using AI** is a production-oriented, full-stack web application designed to bridge the gap between job seekers' current qualifications and market job requirements. 

The application enables candidates to upload resumes (PDF/DOCX), parses and normalizes technical and soft skills, compares candidate competencies against target job roles or custom job descriptions, computes transparent match metrics, identifies critical missing skills, and generates personalized, actionable learning roadmaps.

```mermaid
flowchart TD
    subgraph Client["Frontend Layer (React + Vite)"]
        UI["Modern Responsive UI\n(Bootstrap / Modern CSS)"]
        State["State & Auth Management\n(Context API / Hooks)"]
        ApiClient["API Client\n(Axios with Interceptors)"]
    end

    subgraph Gateway["API & Security Layer (Flask)"]
        CORS["CORS & Security Headers"]
        AuthMiddleware["JWT Authentication\n& RBAC Enforcement"]
        RateLimiter["Rate Limiting\n(Flask-Limiter)"]
        Validation["Request Validation\n(Marshmallow)"]
    end

    subgraph CoreServices["Backend Application Core (Flask Blueprints)"]
        AuthService["Auth Service\n(Password Hashing, Tokens)"]
        ResumeService["Resume Service\n(PyMuPDF, python-docx)"]
        AnalysisService["Analysis Service\n(Orchestration Engine)"]
        JobRoleService["Job Role Service\n(Requirements Catalog)"]
        ReportService["Report Service\n(PDF Generation)"]
    end

    subgraph AIEngine["AI & NLP Processing Pipeline"]
        Extractor["Skill Extractor\n(Dictionary & spaCy NLP)"]
        Normalizer["Skill Normalizer\n(Alias Mapping & Canonical IDs)"]
        SemanticMatcher["Semantic Similarity\n(Sentence Transformers / Cosine)"]
        Scorer["Match Scorer\n(Deterministic & Weighted)"]
        Recommender["Recommendation Engine\n(Actionable Topics & Resources)"]
    end

    subgraph Storage["Persistence Layer (MySQL 8.0)"]
        UserTable[("Users & Auth")]
        JobTable[("Job Roles & Required Skills")]
        ResumeTable[("Resumes Metadata")]
        AnalysisTable[("Analyses & Analysis Skills")]
        ResourceTable[("Learning Resources & Recommendations")]
    end

    UI --> State --> ApiClient
    ApiClient -->|HTTPS / REST API| CORS
    CORS --> RateLimiter --> AuthMiddleware --> Validation
    Validation --> CoreServices

    ResumeService --> Extractor
    AnalysisService --> Normalizer
    AnalysisService --> SemanticMatcher
    AnalysisService --> Scorer
    AnalysisService --> Recommender

    CoreServices --> Storage
```

---

## 2. The 17 Logical Components

The system is partitioned into seventeen distinct, decoupled architectural components:

1. **React Frontend**: Single Page Application (SPA) built with React 18 and Vite, offering responsive design, accessible forms, charts, and analysis workflows.
2. **Flask REST API Backend**: Python application factory serving strictly versioned, stateless RESTful endpoints (`/api/v1/...`).
3. **Authentication Module**: Secure JWT-based authentication featuring token signing, bcrypt password hashing, and user identity injection.
4. **Resume Upload and Validation Module**: MIME-type inspector, magic-byte checker, and size-limiting firewall protecting backend storage from malicious files.
5. **Document Text Extraction Module**: High-fidelity text extractors using `PyMuPDF` for PDF streams and `python-docx` for XML-based Word documents.
6. **Resume Preprocessing Module**: Text normalization pipeline handling whitespaces, hyphenations, special characters, and token boundaries without stripping crucial acronyms (e.g., C++, C#, .NET).
7. **Skill Extraction Module**: Hybrid extractor combining curated canonical dictionaries, regex boundaries, and spaCy PhraseMatcher / EntityRuler.
8. **Skill Normalization Module**: Alias-to-canonical graph resolver that unifies synonyms (e.g., `React`, `ReactJS`, `React.js` $\rightarrow$ `React.js`).
9. **Job-Role and Job-Requirement Module**: Catalog and repository layer managing standardized industry roles, essential skills, and preferred skills.
10. **Skill-Matching Engine**: Transparent comparison engine separating matched skills, missing skills, and extraneous candidate skills.
11. **AI-Based Similarity Module**: Semantic similarity evaluator utilizing sentence embeddings and cosine similarity to map non-exact or descriptive qualifications.
12. **Skill-Gap Calculation Module**: Mathematical scoring engine producing both unweighted and weighted match percentages with algorithm version tracking.
13. **Recommendation Engine**: Curated knowledge base mapping identified missing skills to concrete study topics, practice projects, and verified documentation links.
14. **Career-Role Recommendation Module**: Alternate career discovery engine suggesting related industry roles based on extracted skill overlap.
15. **Report-Generation Module**: Report compiler creating structured dashboard views and downloadable PDF analysis summaries.
16. **MySQL Database**: ACID-compliant relational persistence layer with normalized schemas, foreign-key integrity, and indexed query paths.
17. **Automated Testing Module**: End-to-end test suites covering unit logic, integration endpoints, security boundaries, and extraction accuracy.

---

## 3. End-to-End Data Flow

The lifecycle of an analysis follows a linear, deterministic pipeline:

```mermaid
sequenceDiagram
    autonumber
    actor User as Candidate / User
    participant FE as React Frontend
    participant API as Flask API Gateway
    participant DocSvc as Document Extraction
    participant AISvc as AI/NLP Engine
    participant DB as MySQL Database

    User->>FE: Logs in (email, password)
    FE->>API: POST /api/auth/login
    API->>DB: Query user credentials & verify bcrypt hash
    DB-->>API: User record
    API-->>FE: Return JWT Access Token
    
    User->>FE: Selects Job Role & Uploads Resume (PDF/DOCX)
    FE->>API: POST /api/analyses (multipart/form-data + Bearer Token)
    API->>API: Validate JWT & file signature (magic bytes)
    API->>DocSvc: Extract raw text stream
    DocSvc-->>API: Clean text buffer (memory only)
    
    API->>AISvc: Preprocess & extract candidate skills
    AISvc->>AISvc: Normalize skills via canonical dictionary
    API->>DB: Fetch required & preferred skills for Target Job Role
    DB-->>API: Role Skill Profile
    
    API->>AISvc: Run Skill-Matching Engine & Gap Scorer
    AISvc->>AISvc: Compute unweighted & weighted match %
    AISvc->>AISvc: Query Recommendation Engine for missing gaps
    AISvc-->>API: Match Results, Gaps & Learning Roadmap
    
    API->>DB: Persist Resume metadata, Analysis, and Skill Analysis records
    DB-->>API: Transaction Committed (analysis_id)
    API-->>FE: HTTP 201 Created with Analysis JSON payload
    FE-->>User: Render interactive dashboard & gap breakdown
```

---

## 4. AI & NLP Pipeline Architecture

To guarantee accuracy and avoid LLM hallucinations or unpredictable parsing, skill extraction and matching is built with a multi-tiered architecture:

```mermaid
flowchart LR
    Doc["Raw Document\n(PDF/DOCX)"] --> Stream["Text Stream\nExtractor"]
    Stream --> Pre["Text Cleaner &\nTokenizer"]
    
    subgraph ExtractionStage["Layer 1: Deterministic Extraction"]
        Pre --> Exact["Exact & Alias Matcher\n(Word boundary regex + spaCy)"]
        Exact --> Norm["Canonical Normalizer\n(Alias Dictionary)"]
    end
    
    subgraph SemanticStage["Layer 2: Semantic Similarity (Optional/Fuzzy)"]
        Norm --> Embed["Sentence Embedding\n(Feature Vector)"]
        Embed --> Cosine["Cosine Similarity Matrix\n(Threshold > 0.82)"]
    end
    
    subgraph ScoringStage["Layer 3: Evaluation & Recommendation"]
        Norm --> Gap["Gap Classifier\n(Matched, Missing, Additional)"]
        Cosine --> Gap
        Gap --> Calc["Weighted Match Engine"]
        Calc --> Rec["Roadmap Generator"]
    end
```

### Deterministic vs. Semantic Balance
1. **Deterministic Matching (Primary)**: Guarantees high precision ($>95\%$). Word boundaries `\b` prevent substring collisions (e.g., matching the programming language `C` will not trigger inside `CSS`, `Cloud`, or `Basic`).
2. **Semantic Similarity (Secondary)**: Used to highlight descriptive resume bullets (e.g., "orchestrated container deployments" $\rightarrow$ `Docker / Kubernetes`) with confidence score annotations rather than blindly assuming equivalence.

---

## 5. Security & Privacy Model

Resumes contain Personally Identifiable Information (PII). The application enforces strict data governance:

1. **Zero Raw Resume Disk Retention**: Uploaded documents are read directly from memory streams or immediate temporary buffers that are destroyed upon processing completion.
2. **Strict User Isolation**: All database queries for analyses, resumes, and recommendations filter by `user_id` extracted from the cryptographically verified JWT (`flask_jwt_extended`). A user cannot access or enumerate another user's records.
3. **MIME & Magic Byte Validation**: Filename extensions are never trusted. File headers are checked against standard byte signatures (`%PDF-` for PDFs, `PK\x03\x04` for DOCX).
4. **OWASP Compliance**: Parameterized queries via SQLAlchemy ORM (SQL Injection immunity), password hashing using `bcrypt` (12 work factor rounds), and explicit CORS whitelists.

