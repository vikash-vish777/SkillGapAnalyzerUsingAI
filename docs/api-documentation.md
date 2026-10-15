# REST API Documentation: Skill Gap Analyzer Using AI

## 1. Overview & General Conventions

All endpoints follow strict REST architectural principles:
- **Base URL**: `/api`
- **Payload Format**: `application/json` (except `/api/analyses` and `/api/resumes/upload` which accept `multipart/form-data`)
- **Authentication**: Bearer Token in `Authorization` header (`Authorization: Bearer <jwt_access_token>`)
- **Standard Response Envelope**:
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... },
  "errors": null
}
```
- **Standard Error Envelope**:
```json
{
  "success": false,
  "message": "Validation error or error description",
  "data": null,
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

---

## 2. API Endpoints Catalog

### 2.1. System & Health
- **`GET /api/health`**
  - **Purpose**: System health and DB connectivity check.
  - **Auth**: Public
  - **Response 200 OK**:
    ```json
    {
      "success": true,
      "message": "System is healthy",
      "data": {
        "status": "UP",
        "database": "connected",
        "version": "1.0.0"
      }
    }
    ```

### 2.2. Authentication (`/api/auth`)
- **`POST /api/auth/register`**
  - **Purpose**: Register a new user account.
  - **Auth**: Public
  - **Request Body**:
    ```json
    {
      "full_name": "Jane Doe",
      "email": "jane@example.com",
      "password": "StrongPassword123!"
    }
    ```
  - **Response 201 Created**:
    ```json
    {
      "success": true,
      "message": "User registered successfully",
      "data": {
        "user": {
          "id": 1,
          "full_name": "Jane Doe",
          "email": "jane@example.com"
        },
        "access_token": "eyJhbGciOi..."
      }
    }
    ```
  - **Errors**: 400 Bad Request (Validation failure), 409 Conflict (Email already in use).

- **`POST /api/auth/login`**
  - **Purpose**: Authenticate user and issue JWT token.
  - **Auth**: Public
  - **Request Body**:
    ```json
    {
      "email": "jane@example.com",
      "password": "StrongPassword123!"
    }
    ```
  - **Response 200 OK**:
    ```json
    {
      "success": true,
      "message": "Login successful",
      "data": {
        "user": {
          "id": 1,
          "full_name": "Jane Doe",
          "email": "jane@example.com"
        },
        "access_token": "eyJhbGciOi..."
      }
    }
    ```
  - **Errors**: 401 Unauthorized (Invalid credentials).

- **`POST /api/auth/logout`**
  - **Purpose**: Client-side token teardown / token blocklist check.
  - **Auth**: Protected (Bearer Token)
  - **Response 200 OK**:
    ```json
    {
      "success": true,
      "message": "Successfully logged out"
    }
    ```

### 2.3. Job Roles (`/api/job-roles`)
- **`GET /api/job-roles`**
  - **Purpose**: Retrieve all available job roles with category filters.
  - **Auth**: Public or Protected
  - **Response 200 OK**:
    ```json
    {
      "success": true,
      "data": [
        {
          "id": 1,
          "title": "Full Stack Developer",
          "category": "Software Engineering",
          "description": "Develops frontend and backend systems."
        }
      ]
    }
    ```

- **`GET /api/job-roles/<id>`**
  - **Purpose**: Retrieve specific role details and its complete skill requirements.
  - **Auth**: Public or Protected
  - **Response 200 OK**:
    ```json
    {
      "success": true,
      "data": {
        "id": 1,
        "title": "Full Stack Developer",
        "category": "Software Engineering",
        "description": "Develops frontend and backend systems.",
        "required_skills": [
          {
            "id": 10,
            "name": "React.js",
            "category": "Frontend",
            "requirement_type": "essential",
            "importance_weight": 1.5
          }
        ]
      }
    }
    ```

### 2.4. Resume Upload & Analysis (`/api/analyses`)
- **`POST /api/analyses`**
  - **Purpose**: Upload a resume (PDF/DOCX), select target role (or provide custom job description), and execute full NLP skill gap analysis.
  - **Auth**: Protected (Bearer Token)
  - **Request**: `multipart/form-data`
    - `file`: Binary file (`.pdf` or `.docx`, max 5MB)
    - `job_role_id`: Integer ID of the target job role
    - `custom_job_description`: (Optional) Text string for dynamic analysis
  - **Response 201 Created**:
    ```json
    {
      "success": true,
      "message": "Skill gap analysis completed successfully",
      "data": {
        "analysis_id": 42,
        "job_role": "Full Stack Developer",
        "match_percentage": 75.0,
        "weighted_match_percentage": 78.5,
        "matched_skills": [
          { "name": "React.js", "category": "Frontend", "confidence_score": 1.0, "evidence": "Built web app in React.js" }
        ],
        "missing_skills": [
          { "name": "Docker", "category": "DevOps", "requirement_type": "essential", "importance_weight": 1.2 }
        ],
        "additional_skills": [
          { "name": "GraphQL", "category": "API" }
        ],
        "recommendations": [
          {
            "skill": "Docker",
            "priority": 1,
            "action_steps": "Learn containerization basics, Dockerfile, and docker-compose.",
            "resources": [
              {
                "title": "Docker Getting Started Tutorial",
                "url": "https://docs.docker.com/get-started/",
                "type": "documentation"
              }
            ]
          }
        ],
        "suggested_career_roles": [
          {
            "title": "Frontend Engineer",
            "match_percentage": 90.0,
            "reason": "Strong frontend skill overlap with React.js, CSS, and TypeScript."
          }
        ]
      }
    }
    ```
  - **Errors**: 400 Bad Request (Unsupported MIME type or corrupt file), 404 (Job role not found).

- **`GET /api/analyses`**
  - **Purpose**: Get all historical analyses for the authenticated user.
  - **Auth**: Protected (Bearer Token)
  - **Response 200 OK**:
    ```json
    {
      "success": true,
      "data": [
        {
          "id": 42,
          "job_role_title": "Full Stack Developer",
          "match_percentage": 75.0,
          "created_at": "2026-10-15T19:30:00Z"
        }
      ]
    }
    ```

- **`GET /api/analyses/<id>`**
  - **Purpose**: Retrieve full details of a specific past analysis belonging to the user.
  - **Auth**: Protected (Bearer Token)
  - **Errors**: 403 Forbidden (If analysis belongs to another user), 404 Not Found.

- **`DELETE /api/analyses/<id>`**
  - **Purpose**: Delete a saved analysis record.
  - **Auth**: Protected (Bearer Token)

### 2.5. Reports (`/api/analyses/<id>/report`)
- **`GET /api/analyses/<id>/report?format=pdf`**
  - **Purpose**: Stream downloadable PDF analysis report.
  - **Auth**: Protected (Bearer Token)
  - **Response**: `application/pdf` binary stream with `Content-Disposition: attachment; filename="skill-gap-report-42.pdf"`

### 2.6. User Profile (`/api/users/me`)
- **`GET /api/users/me`**: Get current user profile and summary statistics.
- **`PATCH /api/users/me`**: Update user profile details.
- **`DELETE /api/users/me`**: GDPR-compliant account and data deletion.

