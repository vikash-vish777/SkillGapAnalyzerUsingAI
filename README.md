# 🚀 Skill Gap Analyzer Using Artificial Intelligence (AI)

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-6-646CFF?logo=vite)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)
![Pytest](https://img.shields.io/badge/Tests-47%20Passed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

An enterprise-ready, full-stack AI platform that benchmarks candidate resumes against market job requirements, identifies critical competency gaps, calculates transparent match percentages, and generates personalized learning roadmaps with verified educational resources.

---

# 🌐 Live Application

**Try the deployed application:**

🔗 **Live Website:** https://skill-gap-analyzer-using-ai.vercel.app/

🔗 **Backend API:** https://skill-gap-analyzer-api-oo41.onrender.com

🔗 **API Health Check:** https://skill-gap-analyzer-api-oo41.onrender.com/api/health

**Deployment Status:** Online and operational.

---

# 📑 Table of Contents

* [1. Project Overview & Problem Statement](#1-project-overview--problem-statement)
* [2. System Architecture](#2-system-architecture)
* [3. Key Features](#3-key-features)
* [4. Technology Stack](#4-technology-stack)
* [5. Project Directory Structure](#5-project-directory-structure)
* [6. Local Development Setup](#6-local-development-setup)
* [7. Production Deployment & Cloud Infrastructure](#7-production-deployment--cloud-infrastructure)
* [8. Automated Testing & Quality Assurance](#8-automated-testing--quality-assurance)
* [9. REST API Reference](#9-rest-api-reference)
* [10. Security & Privacy Architecture](#10-security--privacy-architecture)
* [11. Demonstration & Walkthrough](#11-demonstration--walkthrough)
* [12. License](#12-license)

---

## 1. Project Overview & Problem Statement

### The Problem

Job seekers, fresh graduates, and career changers face an opaque hiring market. Automated Applicant Tracking Systems (ATS) reject resumes without constructive feedback, leaving candidates unsure of which essential competencies they lack or what specific skills to acquire to qualify for their desired positions.

### The Solution

**Skill Gap Analyzer Using AI** offers an end-to-end, automated screening and upskilling solution:

* Ingests resumes in PDF and Word DOCX formats without storing private files on disk.
* Extracts technical and soft competencies using boundary-aware NLP and canonical synonym mapping.
* Compares extracted skills against normalized industry job roles.
* Computes both raw match percentage and importance-weighted match scores.
* Quantifies document vocabulary depth using TF-IDF and Cosine Semantic Similarity.
* Generates prioritized, structured learning roadmaps with verified tutorials and documentation.
* Identifies alternative career pathways where candidate skills already align.
* Generates and streams on-demand vector PDF audit reports.

---

## 2. System Architecture

The application follows a three-tier architecture consisting of a React frontend, Flask REST API backend, and MySQL database.

### Architecture Diagram

```text
                  USER / BROWSER
                        |
                        |
                   HTTPS (443)
                        |
                        v
             +----------------------+
             |    VERCEL CLOUD      |
             |                      |
             |    React + Vite      |
             |    Frontend          |
             +----------------------+
                        |
                        |
                 REST API / HTTPS
                        |
                        v
             +----------------------+
             |     RENDER CLOUD     |
             |                      |
             |    Python Flask API  |
             |    Gunicorn Server   |
             |    Docker Container  |
             +----------------------+
                        |
                        |
                    SSL / TLS
                        |
                        v
             +----------------------+
             |     AIVEN CLOUD      |
             |                      |
             |    MySQL Database    |
             +----------------------+
```

### Architecture Components

1. **Frontend Layer:** React.js and Vite provide the user interface.
2. **Backend Layer:** Flask handles business logic, authentication, resume processing, and REST API requests.
3. **AI & NLP Layer:** Scikit-learn and custom NLP logic perform skill extraction and matching.
4. **Database Layer:** MySQL stores user information, job roles, skills, and analysis history.
5. **Deployment Layer:** Vercel, Render, and Aiven provide cloud hosting.

---

## 3. Key Features

1. **Zero-Disk Ingestion & File Signature Protection**

   * Resumes are validated against binary magic bytes (`%PDF-` and `PK\x03\x04`).
   * Disguised executables (`MZ` and `ELF`) are rejected immediately.
   * Text extraction runs entirely in volatile RAM buffers (`io.BytesIO`); raw resumes are never saved to disk.

2. **Hybrid NLP Skill Extraction Engine**

   * Regex patterns with context protection for terms like `C`, `C++`, `C#`, `.NET`, `CI/CD`.
   * Synonym mapping database (e.g. `py`, `python3`, `cpython` → canonical `Python`).
   * Sentence-level evidence capture linking each detected skill to where it appears in the resume.

3. **Deterministic Dual-Score Calculation**

   * **Basic Match %:** Raw count ratio of matched competencies to total required competencies.
   * **Weighted Match %:** Factors in importance weights (`1.0` to `2.0`) differentiating essential requirements from preferred skills.

4. **TF-IDF & Cosine Semantic Similarity Engine**

   * Compares unstructured resume text against target job descriptions.
   * Computes cosine similarity, ratings (High, Moderate, Low), and extracts top shared keywords.

5. **Actionable Learning Roadmaps with Verified Resources**

   * Priority 1 (Essential gaps) vs. Priority 2 (Preferred gaps).
   * Provides importance reasons, core topics, hands-on practice exercises, and verified documentation links.

6. **Alternative Career Pathway Discovery**

   * Calculates cross-role overlap across the catalog, suggesting alternative positions the candidate already qualifies for.

7. **On-Demand High-Fidelity PDF Reports**

   * Assembles clean, publication-ready vector PDF reports with score gauges, competency lists, and roadmap steps streamed directly to the browser.

8. **Multi-Tenant Isolation & Audit Trail**

   * Persists analysis history for authenticated users.
   * Enforces strict user ownership verification (cross-user access returns HTTP 403 Forbidden).
   * Cascading deletions remove child records cleanly.

9. **Abuse Mitigation & Defensive Headers**

   * Rate limiting: 5 req/min on authentication; 10 req/min on resume parsing and analysis.
   * Standard security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`.

---

## 4. Technology Stack

| Layer               | Technologies                                                                       |
| ------------------- | ---------------------------------------------------------------------------------- |
| Frontend            | React 18, Vite 6, Bootstrap 5, Bootstrap Icons, React Router v6, Axios, Chart.js   |
| Backend             | Python 3.13, Flask 3.1, Flask-JWT-Extended, Flask-Limiter, Waitress, Gunicorn      |
| AI & NLP            | scikit-learn, TF-IDF, Cosine Similarity, PyMuPDF, python-docx, Regular Expressions |
| Database            | MySQL 8.0, SQLAlchemy ORM, Flask-Migrate, Alembic, SQLite fallback                 |
| DevOps & Containers | Docker, Docker Compose, Nginx, Vercel SPA routing                                  |
| Testing             | pytest, pytest-flask, Postman API Collection                                       |

---

## 5. Project Directory Structure

```text
SkillGapAnalyzerUsingAI/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── package.json
│   ├── vercel.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── errors/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── __init__.py
│   ├── migrations/
│   ├── tests/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements.txt
│   ├── run.py
│   ├── run_waitress.py
│   └── wsgi.py
│
├── database/
│   ├── schema.sql
│   └── seed_data.py
│
├── docker/
│   └── nginx.conf
│
├── docs/
│   ├── api-documentation.md
│   ├── architecture.md
│   ├── database-design.md
│   ├── deployment-guide.md
│   ├── demonstration-guide.md
│   ├── security-and-privacy.md
│   ├── testing-strategy.md
│   └── postman_collection.json
│
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── LICENSE
└── README.md
```

---

## 6. Local Development Setup

### Prerequisites

* **Python:** Version 3.11, 3.12, or 3.13
* **Node.js:** Version 18.x or 20.x
* **MySQL:** Version 8.0 (or use automated SQLite fallback)
* **Git**
* **VS Code:** Recommended code editor

### 1. Clone Repository

```bash
git clone https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI.git

cd SkillGapAnalyzerUsingAI
```

### 2. Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

Configure environment variables using your local `.env` file.

```env
FLASK_ENV=development

DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=skill_gap_db

USE_SQLITE_FALLBACK=false

SECRET_KEY=your-development-secret
JWT_SECRET_KEY=your-development-jwt-secret

CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 3. Initialize Database & Seed Reference Data

```bash
# Apply database migrations
flask db upgrade

# Seed reference data
python ../database/seed_data.py
```

### 4. Start Backend Server

```bash
# Development server
python run.py

# Or Windows production multi-threaded server
python run_waitress.py
```

Backend API:

```text
http://localhost:5000
```

### 5. Frontend Setup

Open a new terminal.

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start frontend development server
npm run dev
```

Frontend application:

```text
http://localhost:5173
```

---

## 7. Production Deployment & Cloud Infrastructure

### 7.1 Live Production Application

The Skill Gap Analyzer Using AI is deployed using a modern cloud-based architecture with separate frontend, backend, and database services.

| Component        | Cloud Platform | Production URL                                   |
| ---------------- | -------------- | ------------------------------------------------ |
| Frontend         | Vercel         | https://skill-gap-analyzer-using-ai.vercel.app/  |
| Backend REST API | Render         | https://skill-gap-analyzer-api-oo41.onrender.com |
| Database         | Aiven Cloud    | Managed MySQL Database                           |

**Live Application:**

https://skill-gap-analyzer-using-ai.vercel.app/

**Backend API:**

https://skill-gap-analyzer-api-oo41.onrender.com

**API Health Check:**

https://skill-gap-analyzer-api-oo41.onrender.com/api/health

### 7.2 Production Technology & Infrastructure

| Layer              | Technology        | Responsibility                |
| ------------------ | ----------------- | ----------------------------- |
| Frontend Hosting   | Vercel            | React application hosting     |
| Backend Hosting    | Render            | Flask REST API hosting        |
| Application Server | Gunicorn          | Production WSGI server        |
| Database Hosting   | Aiven             | Managed MySQL database        |
| Containerization   | Docker            | Backend application container |
| API Communication  | REST API          | Frontend-backend integration  |
| Security           | HTTPS / SSL / TLS | Secure communication          |

### 7.3 Production API Configuration

**Production API Base URL**

```text
https://skill-gap-analyzer-api-oo41.onrender.com/api
```

**Backend Health Check Endpoint**

```text
https://skill-gap-analyzer-api-oo41.onrender.com/api/health
```

**Successful Health Check Response**

```json
{
  "success": true,
  "message": "Skill Gap Analyzer API is operational",
  "data": {
    "status": "UP",
    "database": "connected",
    "version": "1.0.0"
  },
  "errors": null
}
```

The health-check endpoint verifies backend availability and database connectivity.

### 7.4 Production Environment Configuration

#### Frontend – Vercel

Configure the following environment variable in Vercel:

| Variable            | Value                                                  |
| ------------------- | ------------------------------------------------------ |
| `VITE_API_BASE_URL` | `https://skill-gap-analyzer-api-oo41.onrender.com/api` |

#### Backend – Render

Configure backend environment variables in the Render dashboard.

| Environment Variable | Description                  |
| -------------------- | ---------------------------- |
| `DB_HOST`            | Aiven MySQL hostname         |
| `DB_PORT`            | Aiven MySQL connection port  |
| `DB_NAME`            | Production database name     |
| `DB_USER`            | Database username            |
| `DB_PASSWORD`        | Secure database password     |
| `DB_SSL_CA`          | Mounted SSL certificate path |
| `CORS_ORIGINS`       | Production frontend origin   |
| `SECRET_KEY`         | Flask application secret     |
| `JWT_SECRET_KEY`     | JWT authentication secret    |
| `FLASK_ENV`          | Production environment       |

**Security Note:** Database credentials, application secrets, JWT keys, and private certificates are configured through cloud environment settings. They must never be committed to GitHub.

After changing Vercel environment variables, redeploy the frontend to apply the updated configuration.

### 7.5 Network Ports & Service Configuration

The application uses different network ports for local development, Docker containers, and cloud deployment.

| Service      | Environment       |     Port | Description                     |
| ------------ | ----------------- | -------: | ------------------------------- |
| React + Vite | Local Development |   `5173` | Frontend development server     |
| Flask API    | Local Development |   `5000` | Backend development server      |
| MySQL        | Local Development |   `3306` | Local database server           |
| Nginx        | Docker Deployment |     `80` | Frontend web server             |
| Flask API    | Docker Deployment |   `5000` | Backend API service             |
| Gunicorn     | Render Production | `10000`* | Observed backend listening port |
| Aiven MySQL  | Cloud Database    |  `12526` | Managed MySQL connection        |
| HTTPS        | Cloud Production  |    `443` | Secure web communication        |

#### Port Configuration Details

* **5173:** Vite frontend development server.
* **5000:** Flask backend development server.
* **3306:** Default MySQL local database port.
* **80:** Nginx frontend web server inside Docker.
* **10000:** Port observed for the deployed Render backend. Render provides the `PORT` environment variable, which the application should use.
* **12526:** Configured Aiven MySQL database port.
* **443:** Standard HTTPS port for secure cloud communication.

**Important Notes:**

* Render provides the `PORT` environment variable to the backend service.
* The Gunicorn server should bind to `0.0.0.0:$PORT`.
* Port `10000` is the observed listening port for this deployment, not a universal fixed Render port.
* Production frontend and backend services communicate through public HTTPS endpoints.
* Database connectivity uses the configured Aiven hostname, port, and SSL/TLS settings.

### 7.6 Production System Architecture

The application follows a three-tier cloud deployment architecture.

```text
                 USER / BROWSER
                       |
                       |
                  HTTPS (443)
                       |
                       v
              +-------------------+
              |   VERCEL CLOUD    |
              |                   |
              |   React + Vite    |
              |   Frontend        |
              +-------------------+
                       |
                       |
                REST API / HTTPS
                       |
                       v
              +-------------------+
              |   RENDER CLOUD    |
              |                   |
              |   Python Flask API|
              |   Gunicorn Server |
              |   Docker Container|
              +-------------------+
                       |
                       |
                   SSL / TLS
                       |
                       v
              +-------------------+
              |   AIVEN CLOUD     |
              |                   |
              |   MySQL Database  |
              +-------------------+
```

### 7.7 Production Deployment Workflow

1. Frontend application is built and deployed on Vercel.
2. Backend application is containerized using Docker.
3. Docker-based Flask backend is deployed on Render.
4. MySQL database is hosted on Aiven Cloud.
5. Frontend communicates with the backend through REST APIs.
6. Backend connects to MySQL using SSL/TLS.
7. Database migrations and initial reference data are applied during backend startup.
8. The API health-check endpoint verifies backend and database connectivity.

### 7.8 Docker Deployment

Deploy MySQL, Flask API, and the React/Nginx frontend using Docker Compose.

```bash
docker compose up -d --build
```

Docker deployment endpoints:

| Service                  | URL                              |
| ------------------------ | -------------------------------- |
| Web Application          | http://localhost:80              |
| Backend API Health Check | http://localhost:5000/api/health |

### 7.9 Deployment Status

| Component                    | Deployment Status |
| ---------------------------- | ----------------- |
| React Frontend               | Online            |
| Flask Backend                | Running           |
| REST API                     | Operational       |
| MySQL Database               | Connected         |
| CORS Configuration           | Configured        |
| Cloud Deployment             | Successful        |
| Frontend-Backend Integration | Connected         |

**Final Deployment Result:** Successfully deployed a full-stack AI-powered Skill Gap Analyzer using Vercel, Render, and Aiven Cloud MySQL.

---

## 8. Automated Testing & Quality Assurance

The application features **47 automated tests** covering models, services, document parsing, matching algorithms, authentication, persistence, rate limiting, and edge cases.

### Running the Test Suite

On Windows:

```powershell
cd D:\SkillGapAnalyzerUsingAI

.\backend\.venv\Scripts\pytest.exe backend/tests/ -v
```

### Test Suite Modules

| Test File                             | Test Count | Areas Verified                                                  |
| ------------------------------------- | ---------: | --------------------------------------------------------------- |
| `test_health.py`                      |          2 | Health check endpoint, database connectivity                    |
| `test_models_and_roles.py`            |          4 | Database relationships, cascading deletes, job roles            |
| `test_document_service.py`            |          9 | PDF extraction, DOCX extraction, file validation                |
| `test_matching_engine.py`             |          6 | Match percentage, weighted scoring, skill gaps                  |
| `test_recommendations_and_careers.py` |          4 | Learning roadmaps, verified resources, career recommendations   |
| `test_auth.py`                        |          7 | Registration, password hashing, login, JWT                      |
| `test_analyses_persistence.py`        |          3 | Analysis persistence, audit logs, user isolation                |
| `test_edge_cases.py`                  |         12 | Corrupted files, rate limiting, security headers, JWT tampering |
| **Total**                             |     **47** | **Automated test cases**                                        |

---

## 9. REST API Reference

All API routes are prefixed with `/api`.

For comprehensive schemas, see `docs/api-documentation.md` or import `docs/postman_collection.json`.

| Method   | Endpoint                    | Auth     | Rate Limit | Description                                        |
| -------- | --------------------------- | -------- | ---------- | -------------------------------------------------- |
| `GET`    | `/api/health`               | Public   | None       | Server and database health check                   |
| `POST`   | `/api/auth/register`        | Public   | 5 / min    | Registers user account and returns JWT token       |
| `POST`   | `/api/auth/login`           | Public   | 5 / min    | Authenticates credentials and returns JWT token    |
| `POST`   | `/api/auth/logout`          | JWT      | None       | Client-side session teardown                       |
| `GET`    | `/api/users/me`             | JWT      | None       | Retrieves authenticated user profile               |
| `GET`    | `/api/users/dashboard`      | JWT      | None       | Aggregated scan count, average score, top skill    |
| `GET`    | `/api/job-roles`            | Public   | None       | Lists all standard target job roles                |
| `GET`    | `/api/job-roles/<id>`       | Public   | None       | Fetches target role with required skill weights    |
| `POST`   | `/api/resumes/upload`       | Public   | 10 / min   | In-memory text extraction and preview snippet      |
| `POST`   | `/api/analyses`             | Optional | 10 / min   | Full skill gap analysis, roadmaps, and persistence |
| `GET`    | `/api/analyses`             | JWT      | None       | Retrieves user's past analysis history             |
| `GET`    | `/api/analyses/<id>`        | JWT      | None       | Retrieves detailed breakdown with ownership check  |
| `GET`    | `/api/analyses/<id>/report` | JWT      | None       | Streams downloadable in-memory vector PDF report   |
| `DELETE` | `/api/analyses/<id>`        | JWT      | None       | Deletes analysis record with cascading deletes     |

---

## 10. Security & Privacy Architecture

* **Zero-Disk Retention Policy:** Raw resumes are processed in RAM stream buffers and discarded immediately. No resume files are ever written to disk.
* **Credential Protection:** Passwords are hashed with bcrypt; plain-text passwords are never stored or logged.
* **JWT Authorization:** Cryptographically signed tokens with 24-hour expiration and separate secret keys.
* **Resource Ownership Enforcement:** Enforces user identity checks on all `/api/analyses/*` routes; cross-user attempts return HTTP 403 Forbidden.
* **Abuse Prevention:** Rate limiting via Flask-Limiter blocks brute-force attacks (5 requests/minute on login).
* **Defensive Headers:** Enforces `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and `X-XSS-Protection: 1; mode=block`.

For additional details, see `docs/security-and-privacy.md`.

---

## 11. Demonstration & Walkthrough

To review the interactive end-to-end demonstration script, presentation guidelines, and technical interview talking points, refer to:

* **Demonstration & Presentation Guide:** `docs/demonstration-guide.md`
* **API Documentation:** `docs/api-documentation.md`
* **Postman API Test Collection:** `docs/postman_collection.json`
* **Architecture Documentation:** `docs/architecture.md`
* **Database Design:** `docs/database-design.md`

### Live Project Demonstration

**Application:** https://skill-gap-analyzer-using-ai.vercel.app/

**Backend Health Check:** https://skill-gap-analyzer-api-oo41.onrender.com/api/health

---

## 12. License

This project is licensed under the MIT License.

See the [LICENSE](https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI/blob/main/LICENSE) file for details.

---

**Developed by Vikash Vishwakarma**

GitHub: https://github.com/vikash-vish777

Project Repository: https://github.com/vikash-vish777/SkillGapAnalyzerUsingAI
