# Security and Privacy Architecture

## 1. Overview and Security Principles

The **Skill Gap Analyzer Using AI** adheres to strict security, privacy, and defensive engineering standards. Because the platform processes personal data (candidate resumes, names, career histories, and skill sets), security and privacy-by-design are central to every tier of the application.

Core security objectives:
1. **Zero-Disk Raw Document Retention**: Candidate resumes are processed strictly in RAM and never written to permanent disk storage.
2. **Confidentiality & Access Control**: Strong password hashing (bcrypt), signed JSON Web Tokens (JWT), and strict multi-tenant user isolation.
3. **Abuse & DoS Mitigation**: IP-based rate limiting on sensitive routes to protect against brute-force attacks and resource exhaustion.
4. **Data Integrity & Validation**: Strict magic-byte file signature validation, size limits, and sanitization before processing.
5. **Information Leakage Prevention**: Standardized error handling masking internal exceptions and database details from clients.

---

## 2. Zero-Disk Raw Document Retention Policy

### Data Ingestion and Volatility
- When a candidate uploads a resume (PDF or DOCX), the byte stream is received via HTTP multipart/form-data.
- In `DocumentService.validate_and_read`, the file stream is read entirely into volatile RAM (`io.BytesIO`).
- Parsing and text extraction are performed in-memory using `pymupdf` (for PDF) and `python-docx` (for DOCX).
- Once text is extracted and normalized:
  - The in-memory byte buffer is released to Python's garbage collector.
  - Raw binary documents and original full-text bodies are **never saved to the database or written to disk**.
  - Only normalized metadata (extracted skill names, match scores, timestamp, and target role ID) is saved in the database for the user's personal audit trail.

### Retention Lifecycle
| Data Element | Storage Location | Retention Duration |
| :--- | :--- | :--- |
| Uploaded PDF/DOCX Binary | Volatile RAM | Dropped immediately upon extraction |
| Unstructured Text Stream | Volatile RAM | Dropped immediately after skill extraction |
| Extracted Competency Metadata | MySQL Database | Persisted until explicitly deleted by user |
| Downloadable PDF Report | Generated On-Demand in RAM | Streamed over HTTPS, zero disk retention |

---

## 3. Authentication & Credential Security

### Password Hashing
- Passwords are encrypted using **bcrypt** with a minimum work factor of 12 salt rounds via `werkzeug.security` (`generate_password_hash` with `scrypt`/`pbkdf2:sha256` or `bcrypt`).
- Plain-text passwords are never stored, logged, or included in API error responses.

### Token-Based Authentication (JWT)
- Authenticated sessions use cryptographically signed **JSON Web Tokens (JWT)** via `flask_jwt_extended`.
- Default token lifespan: **1440 minutes (24 hours)** in production; configurable via `JWT_ACCESS_TOKEN_EXPIRES_MINUTES`.
- Secret key isolation: `JWT_SECRET_KEY` and `SECRET_KEY` are decoupled and injected exclusively through environment variables.
- Token tampering protection: Tokens with altered signatures, expired lifetimes, or invalid formats are rejected with HTTP 401/422.

---

## 4. Rate Limiting & Brute-Force Prevention

To guard against denial-of-service, automated credential stuffing, and resource exhaustion, rate limiting is applied via `Flask-Limiter` with an in-memory or Redis key-value store.

### Route-Level Limits
| Endpoint | Method | Rate Limit | Purpose |
| :--- | :--- | :--- | :--- |
| `/api/auth/login` | POST | `5 per minute` | Prevents automated credential stuffing & password brute-force |
| `/api/auth/register` | POST | `5 per minute` | Prevents automated account creation and bot spam |
| `/api/resumes/upload` | POST | `10 per minute` | Prevents document parsing pipeline overload |
| `/api/analyses` | POST | `10 per minute` | Guards CPU-intensive NLP and semantic vectorization pipelines |
| Global Default | ANY | `200/day, 50/hour`| Baseline IP abuse mitigation |

### Rate Limit Response Format
When limits are exceeded, the API responds with HTTP 429 Too Many Requests:
```json
{
  "success": false,
  "message": "Rate limit exceeded: 5 per 1 minute",
  "data": null,
  "errors": null
}
```

---

## 5. File Upload & Magic-Byte Validation

To prevent malicious executable uploads masked as harmless documents (e.g., `malware.exe` renamed to `resume.pdf`), `DocumentService` enforces multi-layer inspection:

1. **Extension Check**: Restricts uploads strictly to `.pdf` and `.docx`.
2. **File Size Enforcement**: Hard limit of **5 MB** (`MAX_FILE_SIZE = 5 * 1024 * 1024`). Files exceeding this are rejected before extraction.
3. **Magic-Byte Signature Verification**:
   - PDF files must begin with `%PDF-` (`0x25 0x50 0x44 0x46 0x2D`).
   - Word DOCX files must begin with the ZIP signature `PK\x03\x04` (`0x50 0x4B 0x03 0x04`) and must contain a verified `word/document.xml` internal structure.
4. **Executable Blocking**: Immediate rejection if file headers contain `MZ` (Windows PE executable) or `\x7fELF` (Linux binary).
5. **Encryption Protection**: Encrypted or password-protected PDFs are rejected immediately.

---

## 6. Defensive HTTP Headers

All HTTP responses from the Flask backend automatically include modern defensive headers via an `@app.after_request` filter:

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

- **`X-Content-Type-Options: nosniff`**: Prevents browsers from MIME-sniffing responses away from the declared content-type.
- **`X-Frame-Options: DENY`**: Protects against clickjacking by preventing the API from being embedded in `<iframe>`, `<frame>`, or `<object>`.
- **`X-XSS-Protection: 1; mode=block`**: Enables cross-site scripting filters in legacy user agents.
- **`Referrer-Policy: strict-origin-when-cross-origin`**: Protects sensitive query parameters from leaking across cross-origin requests.

---

## 7. Multi-Tenant Data Isolation & Privacy

### Resource Ownership
- Every persisted analysis and resume record is tied to a verified `user_id`.
- The API explicitly enforces ownership checks before returning or modifying sensitive records:
  - `GET /api/analyses/<id>`: Returns HTTP 403 Forbidden if `analysis.user_id != current_user_id`.
  - `DELETE /api/analyses/<id>`: Returns HTTP 403 Forbidden if `analysis.user_id != current_user_id`.
  - `GET /api/analyses/<id>/report`: Streamed PDF is inaccessible to non-owners (HTTP 403 Forbidden).

### Cascading Deletion
- When a user deletes an analysis, all associated `analysis_skills`, `recommendations`, and `resumes` records are removed cleanly via SQLAlchemy cascading foreign key constraints (`ondelete="CASCADE"`).

---

## 8. OWASP Top 10 Mitigation Matrix

| Vulnerability | Mitigation Strategy in Skill Gap Analyzer |
| :--- | :--- |
| **A01: Broken Access Control** | JWT authentication, user identity validation on all `/api/analyses/*` and `/api/users/*` endpoints, HTTP 403 for cross-user resource access. |
| **A02: Cryptographic Failures** | Bcrypt password hashing (minimum 12 rounds), HTTPS enforced in production, isolated secret keys via `.env`. |
| **A03: Injection (SQL / Command)** | 100% parameterized SQL queries via SQLAlchemy ORM; zero raw string concatenation; zero shell command execution. |
| **A04: Insecure Design** | Zero-disk raw document retention, memory-only stream processing, deterministic gap calculations. |
| **A05: Security Misconfiguration** | Defensive HTTP headers, disabled debug mode in production, explicit CORS whitelists via `CORS_ORIGINS`. |
| **A06: Vulnerable & Outdated Components** | Pinned modern library versions (Flask 3.1, PyMuPDF 1.28, python-docx 1.2, scikit-learn 1.9, React 19). |
| **A07: Identification & Auth Failures** | Rate limiting on `/api/auth/login` (5/min), strong password regex requirements (minimum 8 characters), strict JWT verification. |
| **A08: Software & Data Integrity Failures** | Magic-byte signature checking (`%PDF-`, `PK\x03\x04`), rejection of disguised executables (`MZ`, `ELF`). |
| **A09: Security Logging & Monitoring** | Standardized JSON error handlers, structured server logs without leaking passwords, tokens, or personal identifiers. |
| **A10: Server-Side Request Forgery (SSRF)** | Static verified learning resource URLs; no dynamic server-side fetching of arbitrary user-submitted external URLs. |
