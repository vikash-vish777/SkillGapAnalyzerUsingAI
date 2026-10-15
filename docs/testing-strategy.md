# Testing Strategy: Skill Gap Analyzer Using AI

## 1. Quality Assurance Philosophy

The system enforces high testing coverage across both backend deterministic logic (parsing, regex, scoring calculations) and API integration flows (authentication, authorization, multipart uploads, database persistence).

---

## 2. Testing Levels & Matrix

| Level | Scope | Tools | Key Targets |
| :--- | :--- | :--- | :--- |
| **Unit Testing** | Backend AI / NLP modules & utility functions | `pytest` | Skill extraction, alias normalization, boundary isolation (no false positives for `C`), weighted scoring formula |
| **Integration Testing** | Flask API endpoints & Database layer | `pytest`, Flask test client, SQLite/MySQL test DB | Auth registration/login, JWT enforcement, resume upload validation, analyses persistence, isolation between users |
| **Frontend Testing** | React components & custom hooks | Vitest, React Testing Library | Form validations, token storage, API error states, dynamic charts, upload dropzones |
| **End-to-End & Manual** | Full user flow | Browser, Postman, test fixtures | Real PDF/DOCX uploads, edge cases (corrupt files, empty files, non-technical resumes) |

---

## 3. Unit Test Cases (AI & NLP Focus)

1. **False-Positive Prevention**:
   - Verify that resume text containing "Basic knowledge of Cloud Computing" does NOT trigger the programming language `C`.
   - Verify that "Experience in Go-to-market strategy" does NOT trigger the programming language `Go`.
2. **Alias Unification**:
   - Verify that `React`, `ReactJS`, `React.js` all resolve to canonical skill `React.js`.
   - Verify that `Node`, `Node.js`, `NodeJS` resolve to canonical skill `Node.js`.
3. **Scoring Formula Integrity**:
   - Test basic match percentage: $(M / R) \times 100$.
   - Test weighted percentage: $(\sum W_{\text{matched}} / \sum W_{\text{total}}) \times 100$.
   - Edge case: Zero requirements handled gracefully without zero-division error.
4. **Document Parsers**:
   - Valid text extraction from standard PDF.
   - Valid text extraction from standard DOCX.
   - Graceful error handling for encrypted or malformed files.

---

## 4. Integration & Security Test Cases

1. **User Data Isolation**:
   - User A cannot access `/api/analyses/<id_of_user_b>`. Returns HTTP 403 / 404.
2. **File Upload Security**:
   - File greater than 5MB rejected with HTTP 413.
   - Executable `.exe` renamed to `.pdf` rejected via magic byte inspection.
3. **Authentication Lifecycles**:
   - Unauthenticated requests to protected endpoints return HTTP 401.
   - Tampered JWT signature returns HTTP 401.
