# Skill Gap Analyzer Using Artificial Intelligence (AI)

[Python](https://www.python.org/)
([image](https://camo.githubusercontent.com/9a420124897bf8d2fcb64b785ec47da456f7b12d0838cfb225cc283c8acd9fe2/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d332e31332d626c75652e7376673f6c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465))
[Flask](https://flask.palletsprojects.com/)
([image](https://camo.githubusercontent.com/1b629ccf414fc934ae59fa1f3a8cf2cb1eb3380392f344000acd9e65fea3b048/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f466c61736b2d332e312d626c61636b2e7376673f6c6f676f3d666c61736b266c6f676f436f6c6f723d7768697465))
[React](https://react.dev/)
([image](https://camo.githubusercontent.com/1b641b1e41bd9b5802e596132eabcc2375c2369f56949fc1749492feae1422b3/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f52656163742d31382d3631444146422e7376673f6c6f676f3d7265616374266c6f676f436f6c6f723d626c61636b))
[Vite](https://vitejs.dev/)
([image](https://camo.githubusercontent.com/1ac8e2fec8763ed83b60a4d5800c666edc51f731df7e430622479d15782b88c4/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f566974652d362e302d3634364346462e7376673f6c6f676f3d76697465266c6f676f436f6c6f723d7768697465))
[MySQL](https://www.mysql.com/)
([image](https://camo.githubusercontent.com/69979642462159a0235efbcd5c9807a4659fd4e0a79c4bb0e47043f47b82e9e1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4d7953514c2d382e302d3434373941312e7376673f6c6f676f3d6d7973716c266c6f676f436f6c6f723d7768697465))
[Docker](https://www.docker.com/)
([image](https://camo.githubusercontent.com/79f502fb63b3a0ba131ee949be0474368163aacdb62ed57f053533eebd0b2129/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f636b65722d456e61626c65642d3234393645442e7376673f6c6f676f3d646f636b6572266c6f676f436f6c6f723d7768697465))
[Pytest](https://docs.pytest.org/)
([image](https://camo.githubusercontent.com/5954c06e3d307c7cbefc2c2831b1f70e41cfaa0f5f96f28469f4193ff87be878/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f54657374732d343725323050617373656425323028313030253235292d627269676874677265656e2e7376673f6c6f676f3d707974657374266c6f676f436f6c6f723d7768697465))
[License:
MIT](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI/blob/main/LICENSE)
([image](https://camo.githubusercontent.com/fdf2982b9f5d7489dcf44570e714e3a15fce6253e0cc6b5aa61a075aac2ff71b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d79656c6c6f772e737667))

An enterprise-ready, full-stack AI platform that benchmarks candidate
resumes against market job requirements, identifies critical competency
gaps, calculates transparent match percentages, and generates
personalized learning roadmaps with verified educational resources.

------------------------------------------------------------------------

## Table of Contents

-   [1. Project Overview & Problem
    Statement](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#1-project-overview--problem-statement)
-   [2. System
    Architecture](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#2-system-architecture)
-   [3. Key
    Features](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#3-key-features)
-   [4. Technology
    Stack](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#4-technology-stack)
-   [5. Project Directory
    Structure](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#5-project-directory-structure)
-   [6. Local Development
    Setup](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#6-local-development-setup)
-   [7. Production Deployment (Docker &
    Cloud)](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#7-production-deployment-docker--cloud)
-   [8. Automated Testing & Quality
    Assurance](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#8-automated-testing--quality-assurance)
-   [9. REST API
    Reference](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#9-rest-api-reference)
-   [10. Security & Privacy
    Architecture](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#10-security--privacy-architecture)
-   [11. Demonstration &
    Walkthrough](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#11-demonstration--walkthrough)
-   [12.
    License](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI#12-license)

------------------------------------------------------------------------

## 1. Project Overview & Problem Statement

### The Problem

Job seekers, fresh graduates, and career changers face an opaque hiring
market. Automated Applicant Tracking Systems (ATS) reject resumes
without constructive feedback, leaving candidates unsure of which
essential competencies they lack or what specific skills to acquire to
qualify for their desired positions.

### The Solution

**Skill Gap Analyzer Using AI** offers an end-to-end, automated
screening and upskilling solution:

-   Ingests resumes in PDF and Word DOCX formats without storing private
    files on disk.
-   Extracts technical and soft competencies using boundary-aware NLP
    and canonical synonym mapping.
-   Compares extracted skills against normalized industry job roles.
-   Computes both raw match percentage and importance-weighted match
    scores.
-   Quantifies document vocabulary depth using TF-IDF and Cosine
    Semantic Similarity.
-   Generates prioritized, structured learning roadmaps with verified
    tutorials and documentation.
-   Identifies alternative career pathways where candidate skills
    already align.
-   Generates and streams on-demand vector PDF audit reports.

------------------------------------------------------------------------

## 2. System Architecture

[File
display](https://viewscreen.githubusercontent.com/markdown/mermaid?docs_host=https%3A%2F%2Fdocs.github.com&color_mode=dark#6adc6cba-92c0-4c57-b1db-3829153b6c88)

------------------------------------------------------------------------

## 3. Key Features

1.  **Zero-Disk Ingestion & File Signature Protection**:
    -   Resumes are validated against binary magic bytes (`%PDF-` and
        `PK\x03\x04`).
    -   Disguised executables (`MZ` and `ELF`) are rejected immediately.
    -   Text extraction runs entirely in volatile RAM buffers
        (`io.BytesIO`); raw resumes are never saved to disk.
2.  **Hybrid NLP Skill Extraction Engine**:
    -   Regex patterns with context protection for terms like `C`,
        `C++`, `C#`, `.NET`, `CI/CD`.
    -   Synonym mapping database (e.g. `py`, `python3`, `cpython` `→`
        canonical `Python`).
    -   Sentence-level evidence capture linking each detected skill to
        where it appears in the resume.
3.  **Deterministic Dual-Score Calculation**:
    -   **Basic Match %**: Raw count ratio of matched competencies to
        total required competencies.
    -   **Weighted Match %**: Factors in importance weights (`1.0` to
        `2.0`) differentiating essential requirements from preferred
        skills.
4.  **TF-IDF & Cosine Semantic Similarity Engine**:
    -   Compares unstructured resume text against target job
        descriptions.
    -   Computes cosine similarity, ratings (High, Moderate, Low), and
        extracts top shared keywords.
5.  **Actionable Learning Roadmaps with Verified Resources**:
    -   Priority 1 (Essential gaps) vs. Priority 2 (Preferred gaps).
    -   Provides importance reasons, core topics, hands-on practice
        exercises, and verified documentation links.
6.  **Alternative Career Pathway Discovery**:
    -   Calculates cross-role overlap across the catalog, suggesting
        alternative positions the candidate already qualifies for.
7.  **On-Demand High-Fidelity PDF Reports**:
    -   Assembles clean, publication-ready vector PDF reports with score
        gauges, competency lists, and roadmap steps streamed directly to
        the browser.
8.  **Multi-Tenant Isolation & Audit Trail**:
    -   Persists analysis history for authenticated users.
    -   Enforces strict user ownership verification (cross-user access
        returns HTTP 403 Forbidden).
    -   Cascading deletions remove child records cleanly.
9.  **Abuse Mitigation & Defensive Headers**:
    -   Rate limiting: 5 req/min on authentication; 10 req/min on resume
        parsing and analysis.
    -   Standard security headers: `X-Content-Type-Options: nosniff`,
        `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`.

------------------------------------------------------------------------

## 4. Technology Stack

  -------------------------------------------------------------------------
  **Layer**      **Technologies**
  -------------- ----------------------------------------------------------
  **Frontend**   React 18, Vite 6, Bootstrap 5, Bootstrap Icons, React
                 Router v6, Axios, Chart.js

  **Backend**    Python 3.13, Flask 3.1 (Application Factory, Blueprints),
                 Flask-JWT-Extended, Flask-Limiter, Waitress, Gunicorn

  **AI & NLP**   scikit-learn (TF-IDF, Cosine Similarity), PyMuPDF 1.25+
                 (MuPDF C-engine), python-docx, regular expressions

  **Database**   MySQL 8.0, SQLAlchemy 3.1 ORM, Flask-Migrate (Alembic),
                 SQLite (automated fallback)

  **DevOps &     Docker, Docker Compose, Nginx (Alpine), Vercel SPA routing
  Containers**   

  **Testing**    pytest 8.3, pytest-flask, Postman API Collection (v2.1)
  -------------------------------------------------------------------------

------------------------------------------------------------------------

## 5. Project Directory Structure

    SkillGapAnalyzerUsingAI/
    │
    ├── frontend/                     # React 18 + Vite frontend
    │   ├── public/                   # Static public assets
    │   ├── src/
    │   │   ├── components/           # Reusable UI components (Navbar, Footer, etc.)
    │   │   ├── context/              # AuthContext session management
    │   │   ├── pages/                # Page views (Home, Login, Register, Dashboard, Analyze, Results, History)
    │   │   ├── services/             # Axios API client with JWT interceptor
    │   │   ├── App.jsx               # Client-side router configuration
    │   │   └── main.jsx              # React DOM entrypoint
    │   ├── Dockerfile                # Multi-stage build (Node 20 builder -> Nginx alpine)
    │   ├── package.json              # Frontend npm dependencies
    │   ├── vercel.json               # Vercel SPA routing rewrites
    │   └── vite.config.js            # Vite build configuration
    │
    ├── backend/                      # Flask REST API backend
    │   ├── app/
    │   │   ├── ai/                   # NLP extractor, preprocessor, normalizer, semantic matcher
    │   │   ├── errors/               # Standardized error handlers and custom exceptions
    │   │   ├── models/               # 9 Normalized SQLAlchemy database models
    │   │   ├── routes/               # Modular API blueprints (auth, users, job-roles, resumes, analyses)
    │   │   ├── services/             # Document parsing, matching engine, recommendations, PDF generator
    │   │   ├── config.py             # Configuration classes (Dev, Testing, Prod)
    │   │   ├── extensions.py         # Extension singletons (db, jwt, limiter, cors)
    │   │   └── __init__.py           # Application factory with defensive security headers
    │   ├── migrations/               # Alembic database migration versions
    │   ├── tests/                    # 47 automated tests (persistence, auth, parsing, edge cases)
    │   ├── Dockerfile                # Production Python 3.13-slim container
    │   ├── entrypoint.sh             # Startup script: DB wait, migration check, seed, Gunicorn
    │   ├── requirements.txt          # Python dependencies
    │   ├── run.py                    # Local development runner
    │   ├── run_waitress.py           # Native Windows multi-threaded WSGI runner
    │   └── wsgi.py                   # Production WSGI entrypoint
    │
    ├── database/
    │   ├── schema.sql                # Complete 3NF DDL schema with constraints & indexes
    │   └── seed_data.py              # Reference seeder (5 roles, 31 canonical skills, verified resources)
    │
    ├── docker/
    │   └── nginx.conf                # Production Nginx reverse proxy & SPA server
    │
    ├── docs/                         # Professional documentation
    │   ├── api-documentation.md      # Full REST API contracts and JSON schemas
    │   ├── architecture.md           # System architecture & component design
    │   ├── database-design.md        # Normalized database schema & ERD
    │   ├── deployment-guide.md       # Multi-platform deployment guide (Cloud, Docker, Windows)
    │   ├── demonstration-guide.md    # Step-by-step presentation script & interview defenses
    │   ├── security-and-privacy.md   # Zero-disk retention, bcrypt, JWT & OWASP mitigation matrix
    │   ├── testing-strategy.md       # QA methodologies & test suite documentation
    │   └── postman_collection.json   # Exportable Postman API test collection
    │
    ├── docker-compose.yml            # Multi-container orchestration (MySQL + Backend + Frontend)
    ├── .dockerignore                 # Root build context ignore rules
    ├── .gitignore                    # Git tracking ignore rules
    ├── LICENSE                       # MIT License
    └── README.md                     # Comprehensive project documentation

------------------------------------------------------------------------

## 6. Local Development Setup

### Prerequisites

-   **Python**: Version 3.11, 3.12, or 3.13
-   **Node.js**: Version 18.x or 20.x
-   **MySQL**: Version 8.0 (or use automated SQLite fallback)
-   **Git**

### 1. Clone Repository

    git clone https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI.git
    cd SkillGapAnalyzerUsingAI

### 2. Backend Setup

    # Create and activate virtual environment
    cd backend
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1   # On Linux/macOS: source .venv/bin/activate

    # Install dependencies
    pip install --upgrade pip
    pip install -r requirements.txt

    # Configure environment variables
    cp .env.example .env

Ensure `.env` matches your MySQL credentials:

    FLASK_ENV=development
    DB_USER=root
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=3306
    DB_NAME=skill_gap_db
    USE_SQLITE_FALLBACK=false
    SECRET_KEY=dev-secret-key-skill-gap
    JWT_SECRET_KEY=dev-jwt-secret-key
    CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

### 3. Initialize Database & Seed Reference Data

    # Apply database migrations
    flask db upgrade

    # Seed 5 standard roles, 31 canonical skills, and verified resources
    python ../database/seed_data.py

### 4. Start Backend Server

    # Development server (with hot reload)
    python run.py

    # Or Windows production multi-threaded server (Waitress)
    python run_waitress.py

The API will be live at `http://localhost:5000`.

### 5. Frontend Setup

In a new terminal:

    cd frontend
    npm install
    npm run dev

The web application will be live at `http://localhost:5173`.

------------------------------------------------------------------------

## 7. Production Deployment (Docker & Cloud)

### Live Production Environment

The application is deployed as a three-tier cloud solution:

  --------------------------------------------------------------------------------------------------------
  Layer             Platform          Production URL                                     Responsibility
  ----------------- ----------------- -------------------------------------------------- -----------------
  Frontend          Vercel            https://skill-gap-analyzer-using-ai.vercel.app/    React + Vite web
                                                                                         application

  Backend API       Render            https://skill-gap-analyzer-api-oo41.onrender.com   Flask REST API

  Database          Aiven for MySQL   Managed database connection                        User accounts,
                                                                                         job-role data,
                                                                                         and analysis
                                                                                         history
  --------------------------------------------------------------------------------------------------------

**Production API base URL**

``` text
https://skill-gap-analyzer-api-oo41.onrender.com/api
```

**Backend health check**

``` text
https://skill-gap-analyzer-api-oo41.onrender.com/api/health
```

A successful health check confirms that the API is responding and
reports database connectivity. Keep database credentials, private
certificates, and application secrets in the hosting provider's
environment settings. Never commit them to Git.

#### Production environment variables

  --------------------------------------------------------------------------------------------------------
  Platform                Variable                Configuration
  ----------------------- ----------------------- --------------------------------------------------------
  Vercel                  `VITE_API_BASE_URL`     `https://skill-gap-analyzer-api-oo41.onrender.com/api`

  Render                  `DB_HOST`               Aiven MySQL hostname

  Render                  `DB_PORT`               Aiven MySQL service port

  Render                  `DB_NAME`               Production database name

  Render                  `DB_USER`               Database username

  Render                  `DB_PASSWORD`           Database password; keep private

  Render                  `DB_SSL_CA`             Mounted Aiven CA certificate path, if configured

  Render                  `CORS_ORIGINS`          `https://skill-gap-analyzer-using-ai.vercel.app`

  Render                  `SECRET_KEY`            Strong private Flask secret

  Render                  `JWT_SECRET_KEY`        Separate strong JWT signing secret
  --------------------------------------------------------------------------------------------------------

After changing a Vercel environment variable, create a new deployment so
the new value is included in the frontend build. Redeploy or restart the
Render service after changing backend environment variables.

#### Production request flow

``` text
Browser
   |
   | HTTPS
   v
Vercel - React + Vite Frontend
   |
   | HTTPS REST API requests
   v
Render - Flask API (Gunicorn)
   |
   | TLS / SSL database connection
   v
Aiven - Managed MySQL Database
```

### Option A: Turnkey Single-Command Docker Deployment

Deploy MySQL 8.0, the Flask API, and the React/Nginx frontend on any
server:

    docker compose up -d --build

-   Web Application: `http://localhost:80`
-   API Health Check: `http://localhost:5000/api/health`

### Network Ports & Service Endpoints

  ------------------------------------------------------------------------------------------------------------
  Component        Environment            Port / Protocol Address or configuration
  ---------------- ---------------- --------------------- ----------------------------------------------------
  React + Vite     Local                           `5173` `http://localhost:5173`
  frontend         development                            

  Flask API        Local                           `5000` `http://localhost:5000`
                   development                            

  MySQL            Local                           `3306` `localhost:3306`, if exposed locally
                   development /                          
                   Docker                                 

  Frontend web     Docker                            `80` `http://localhost:80`
  server           deployment                             

  Backend API      Docker                          `5000` `http://localhost:5000/api`
                   deployment                             

  Backend          Render                `10000` observed Bind to `0.0.0.0:$PORT`; Render supplies `PORT`
  container        production                             

  Frontend         Vercel                     HTTPS `443` `https://skill-gap-analyzer-using-ai.vercel.app/`
                   production                  externally 

  Backend API      Render                     HTTPS `443` `https://skill-gap-analyzer-api-oo41.onrender.com`
                   production                  externally 

  MySQL database   Aiven production               `12526` Use the host and port shown in the Aiven service
                                                          details
  ------------------------------------------------------------------------------------------------------------

**Port configuration notes**

-   `5173`, `5000`, and `3306` are the documented local development
    defaults; actual values may differ if local configuration is
    changed.
-   The public Vercel and Render URLs use HTTPS. Users do not need to
    add port numbers to those URLs.
-   Render provides the `PORT` environment variable. Configure Gunicorn
    to bind to `0.0.0.0:$PORT`. Port `10000` is the port observed for
    this deployment, not a universal Render default.
-   The Aiven port is specific to this hosted database service. Use
    TLS/SSL and restrict database access.
-   Never publish database passwords, JWT secrets, Flask secrets,
    private certificates, or `.env` files.

### Option B: Cloud PaaS (Vercel + Render + Managed MySQL)

1.  **Database**: Provision MySQL on AWS RDS, Aiven, or Railway; run
    `database/schema.sql`.
2.  **Backend**: Deploy `backend/` to Render/Railway as a Web Service
    running `gunicorn -w 4 -b 0.0.0.0:$PORT "wsgi:app"`.
3.  **Frontend**: Import `frontend/` into Vercel. Set
    `VITE_API_BASE_URL=https://your-api.onrender.com/api`. *For full
    instructions, see Production Deployment Guide.*

------------------------------------------------------------------------

## 8. Automated Testing & Quality Assurance

The application features **47 comprehensive automated tests** with 100%
pass coverage across models, services, document parsing, matching
algorithms, authentication, persistence, rate limiting, and edge cases.

### Running the Test Suite

    cd D:\SkillGapAnalyzerUsingAI
    .\backend\.venv\Scripts\pytest.exe backend/tests/ -v

### Test Suite Modules

  --------------------------------------------------------------------------------------------------
  **Test File**                           **Test    **Areas Verified**
                                          Count**   
  --------------------------------------- --------- ------------------------------------------------
  `test_health.py`                        2         Health check endpoint, database ping
                                                    connectivity

  `test_models_and_roles.py`              4         3NF relationships, cascading deletes, job role
                                                    catalog endpoints

  `test_document_service.py`              9         PDF text extraction, DOCX extraction, 5MB limit,
                                                    magic byte validation

  `test_matching_engine.py`               6         Flat match %, weighted scoring, gap
                                                    categorization, boundary conditions

  `test_recommendations_and_careers.py`   4         Priority 1 vs 2 roadmaps, verified resources,
                                                    career advisor overlap

  `test_auth.py`                          7         User registration, password hashing (bcrypt),
                                                    login, JWT issuance, profile

  `test_analyses_persistence.py`          3         Database persistence of analyses, user audit
                                                    logs, cross-user isolation

  `test_edge_cases.py`                    12        Zero-match recipes, 100% matches, corrupted
                                                    PDFs, disguised EXEs, rate limiting, security
                                                    headers, JWT tampering

  **Total**                               **47**    **100% Passing**
  --------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 9. REST API Reference

All API routes are prefixed with `/api`. For comprehensive schemas, see
`docs/api-documentation.md` or import `docs/postman_collection.json`.

  ------------------------------------------------------------------------------------------------
  **Method**   **Endpoint**                  **Auth**   **Rate    **Description**
                                                        Limit**   
  ------------ ----------------------------- ---------- --------- --------------------------------
  `GET`        `/api/health`                 Public     None      Server and database health check

  `POST`       `/api/auth/register`          Public     5 / min   Registers user account and
                                                                  returns JWT token

  `POST`       `/api/auth/login`             Public     5 / min   Authenticates credentials and
                                                                  returns JWT token

  `POST`       `/api/auth/logout`            JWT        None      Client-side session teardown

  `GET`        `/api/users/me`               JWT        None      Retrieves authenticated user
                                                                  profile

  `GET`        `/api/users/dashboard`        JWT        None      Aggregated scan count, average
                                                                  score, top skill

  `GET`        `/api/job-roles`              Public     None      Lists all standard target job
                                                                  roles

  `GET`        `/api/job-roles/<id>`         Public     None      Fetches target role with
                                                                  required skill weights

  `POST`       `/api/resumes/upload`         Public     10 / min  In-memory text extraction and
                                                                  preview snippet

  `POST`       `/api/analyses`               Optional   10 / min  Full skill gap analysis,
                                                                  roadmaps, and persistence

  `GET`        `/api/analyses`               JWT        None      Retrieves user's past analysis
                                                                  history

  `GET`        `/api/analyses/<id>`          JWT        None      Retrieves detailed breakdown
                                                                  with ownership check

  `GET`        `/api/analyses/<id>/report`   JWT        None      Streams downloadable in-memory
                                                                  vector PDF report

  `DELETE`     `/api/analyses/<id>`          JWT        None      Deletes analysis record with
                                                                  cascading deletes
  ------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 10. Security & Privacy Architecture

-   **Zero-Disk Retention Policy**: Raw resumes are processed in RAM
    stream buffers and discarded immediately. No resume files are ever
    written to disk.
-   **Credential Protection**: Passwords hashed with bcrypt (12 salt
    rounds); plain-text passwords never stored or logged.
-   **JWT Authorization**: Cryptographically signed tokens with 24-hour
    expiration; separated secret keys.
-   **Resource Ownership Enforcement**: Enforces user identity checks on
    all `/api/analyses/*` routes; cross-user attempts return HTTP 403
    Forbidden.
-   **Abuse Prevention**: Rate limiting via Flask-Limiter blocks
    brute-force attacks (5 req/min on login).
-   **Defensive Headers**: Enforces `X-Content-Type-Options: nosniff`,
    `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`. *For
    full details, see Security and Privacy Architecture.*

------------------------------------------------------------------------

## 11. Demonstration & Walkthrough

To review the interactive end-to-end demonstration script, presentation
guidelines, and technical interview talking points, refer to:

-   **Demonstration & Presentation Guide**
-   **Postman API Test Collection**

------------------------------------------------------------------------

## 12. License

This project is licensed under the MIT License - see the
[LICENSE](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI/blob/main/LICENSE)
file for details.

