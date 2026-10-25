# Production Deployment Guide

## 1. Overview and Architecture

The **Skill Gap Analyzer Using AI** is designed with a decoupled, modern cloud architecture that supports both containerized orchestrations (Docker / Kubernetes) and serverless / PaaS multi-cloud deployments (Vercel + Render / Railway + Managed MySQL).

```
                      +-----------------------------+
                      |       End User Browser      |
                      +--------------+--------------+
                                     |
                    HTTPS (Port 443) |
                                     v
                 +---------------------------------------+
                 |         React SPA (Vite / Nginx)      |
                 |      Hosted on Vercel or Container    |
                 +-------------------+-------------------+
                                     |
                    REST API (JSON)  | HTTPS
                                     v
                 +---------------------------------------+
                 |          Flask REST API Backend       |
                 |      Gunicorn / Waitress WSGI Server  |
                 +-------------------+-------------------+
                                     |
                                SQL  | Port 3306
                                     v
                 +---------------------------------------+
                 |           MySQL 8.0 Database          |
                 |   AWS RDS / Aiven / Railway / Docker  |
                 +---------------------------------------+
```

---

## 2. Deployment Option A: Cloud Platform (Vercel + Render/Railway + Managed MySQL)

This is the recommended serverless/PaaS setup offering auto-scaling, global CDN distribution, and managed database backups.

### Step 1: Managed MySQL Database Provisioning
1. Provision a MySQL 8.0 database instance on **Aiven**, **Railway**, or **AWS RDS**.
2. Note the connection credentials:
   - `DB_HOST` (e.g., `mysql-project.aivencloud.com`)
   - `DB_PORT` (e.g., `3306` or assigned port)
   - `DB_USER` (e.g., `avnadmin` or `root`)
   - `DB_PASSWORD`
   - `DB_NAME` (e.g., `skill_gap_db`)
3. Connect locally via MySQL Workbench or CLI and execute [`database/schema.sql`](file:///d:/SkillGapAnalyzerUsingAI/database/schema.sql) to create the schema and initial tables.

### Step 2: Deploy Flask Backend to Render / Railway
1. Create a new **Web Service** on [Render](https://render.com) or [Railway](https://railway.app) connected to your GitHub repository.
2. Configure build settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3.13`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn`
   - **Start Command**: `gunicorn -w 4 -k gthread --threads 2 --timeout 120 -b 0.0.0.0:$PORT "wsgi:app"`
3. Configure Environment Variables in the service settings:
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=0
   SECRET_KEY=<generate_random_64_char_secret>
   JWT_SECRET_KEY=<generate_different_64_char_secret>
   JWT_ACCESS_TOKEN_EXPIRES_MINUTES=1440
   DB_HOST=<your_managed_mysql_host>
   DB_PORT=3306
   DB_USER=<your_mysql_user>
   DB_PASSWORD=<your_mysql_password>
   DB_NAME=skill_gap_db
   USE_SQLITE_FALLBACK=false
   CORS_ORIGINS=https://your-skill-gap-frontend.vercel.app
   RATELIMIT_ENABLED=true
   MAX_CONTENT_LENGTH_MB=5
   ```
4. Deploy the service and verify the health check endpoint:
   ```bash
   curl -f https://your-backend-api.onrender.com/api/health
   ```
5. Seed initial canonical skills and job roles:
   In the Render/Railway web shell, run:
   ```bash
   python database/seed_data.py
   ```

### Step 3: Deploy React Frontend to Vercel
1. Import the repository into [Vercel](https://vercel.com).
2. Configure project settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add Environment Variable:
   - `VITE_API_BASE_URL` = `https://your-backend-api.onrender.com/api`
4. The included [`frontend/vercel.json`](file:///d:/SkillGapAnalyzerUsingAI/frontend/vercel.json) automatically configures SPA routing rewrites so navigating directly to routes like `/dashboard` or `/results` loads seamlessly without 404 errors.
5. Deploy and verify the live website URL.

---

## 3. Deployment Option B: Docker Compose (Single-Host Containerization)

Deploy the entire stack (MySQL 8, Flask API, and Nginx/React frontend) with a single command on any VPS or Linux server (Ubuntu, Debian, Amazon Linux).

### Prerequisites
- Docker Engine $\ge 24.0$
- Docker Compose $\ge 2.20$

### Execution Steps
1. Clone repository to your target server:
   ```bash
   git clone https://github.com/your-org/SkillGapAnalyzerUsingAI.git
   cd SkillGapAnalyzerUsingAI
   ```
2. Build and launch all containers in detached mode:
   ```bash
   docker compose up -d --build
   ```
3. Monitor startup logs:
   ```bash
   docker compose logs -f backend
   ```
4. Verify all container services are healthy:
   ```bash
   docker compose ps
   ```
5. Access the application:
   - Web Application: `http://<server-ip>:80`
   - Backend API Health: `http://<server-ip>:5000/api/health`

### Architecture of Docker Compose Services
| Service | Image / Build | Port | Purpose |
| :--- | :--- | :--- | :--- |
| `mysql` | `mysql:8.0` | `3306` | Isolated relational database with persistent named volume `mysql_data` |
| `backend` | `./backend/Dockerfile` | `5000` | Gunicorn WSGI server running Flask 3.1 with 4 workers |
| `frontend` | `./frontend/Dockerfile` | `80` | High-performance Nginx alpine server with SPA rewrites and API reverse proxy |

---

## 4. Deployment Option C: Native Windows Production Hosting

For internal corporate environments running on Windows Server.

### Running with Waitress Production WSGI Server
1. Activate virtual environment:
   ```powershell
   cd D:\SkillGapAnalyzerUsingAI
   .\backend\.venv\Scripts\Activate.ps1
   ```
2. Ensure production environment variables are configured in `backend/.env`.
3. Launch multi-threaded Waitress WSGI runner:
   ```powershell
   python backend/run_waitress.py
   ```
4. Waitress will bind to `http://0.0.0.0:5000` with 8 concurrent worker threads.
5. To run as a background Windows Service, use **NSSM (Non-Sucking Service Manager)**:
   ```powershell
   nssm install SkillGapBackend "D:\SkillGapAnalyzerUsingAI\backend\.venv\Scripts\python.exe" "D:\SkillGapAnalyzerUsingAI\backend\run_waitress.py"
   nssm set SkillGapBackend AppDirectory "D:\SkillGapAnalyzerUsingAI\backend"
   nssm start SkillGapBackend
   ```
6. Serve the production frontend build (`frontend/dist`) via Microsoft IIS or reverse-proxy through IIS URL Rewrite / ARR.

---

## 5. Production Environment Variables Reference

### Backend (`backend/.env`)
| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `FLASK_ENV` | Yes | `production` | Enables production mode optimizations |
| `FLASK_DEBUG` | Yes | `0` | Disables interactive debuggers and traceback leakage |
| `SECRET_KEY` | Yes | - | Secret key used for cryptographic session signing |
| `JWT_SECRET_KEY` | Yes | - | Secret key used to sign and verify JSON Web Tokens |
| `JWT_ACCESS_TOKEN_EXPIRES_MINUTES` | No | `1440` | Token validity duration (1440 min = 24 hours) |
| `DB_HOST` | Yes | `localhost` | MySQL database host or service name |
| `DB_PORT` | No | `3306` | MySQL port |
| `DB_USER` | Yes | `root` | Database username |
| `DB_PASSWORD` | Yes | - | Database user password |
| `DB_NAME` | Yes | `skill_gap_db` | Target database name |
| `USE_SQLITE_FALLBACK` | No | `false` | Fallback to local SQLite when MySQL is unreachable |
| `CORS_ORIGINS` | Yes | `http://localhost:5173` | Comma-separated whitelist of allowed frontend origins |
| `MAX_CONTENT_LENGTH_MB` | No | `5` | Maximum upload file size in megabytes |
| `RATELIMIT_ENABLED` | No | `true` | Enables route-level abuse and brute-force throttling |

### Frontend (`frontend/.env`)
| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | No | `/api` | Base URL for REST API requests. Set to full URL on Vercel |

---

## 6. Post-Deployment Smoke Test Checklist

After deploying the application to staging or production, execute this smoke test sequence:

- [ ] **Health Check**: `GET /api/health` returns `{"status": "healthy"}`.
- [ ] **Job Roles Catalog**: `GET /api/job-roles` returns the 5 seeded roles with required skills.
- [ ] **User Registration**: Register a new user at `/register` and verify receipt of JWT token.
- [ ] **User Login**: Log in with registered credentials at `/login` and verify redirect to `/dashboard`.
- [ ] **Resume Ingestion**: Upload a sample resume PDF on `/analyze`. Verify file signature check passes.
- [ ] **Skill Gap Computation**: Confirm display of match %, essential gaps, and learning roadmaps on `/results`.
- [ ] **Historical Audit**: Navigate to `/history` and verify the analysis record is persisted.
- [ ] **PDF Report Stream**: Click "Download PDF Report" and verify browser downloads valid binary PDF report.
- [ ] **Rate Limiting Check**: Attempt 6 rapid authentication attempts and confirm HTTP 429 response.
- [ ] **Security Headers Check**: Inspect HTTP response headers via browser DevTools or `curl -I` to verify `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY`.

