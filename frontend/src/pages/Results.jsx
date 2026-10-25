import React, { useState, useEffect } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [activeTab, setActiveTab] = useState('matched');

  useEffect(() => {
    // Read from route state or fall back to sessionStorage
    const currentData = location.state?.analysis || JSON.parse(sessionStorage.getItem('current_analysis') || 'null');
    if (!currentData) {
      navigate('/analyze');
    } else {
      setAnalysis(currentData);
    }
  }, [location, navigate]);

  if (!analysis) {
    return (
      <div className="container py-5 text-center">
        <div className="spinner-border text-primary" role="status"></div>
        <p className="mt-2 text-muted">Loading your analysis report...</p>
      </div>
    );
  }

  const {
    job_role,
    match_percentage,
    weighted_match_percentage,
    total_required_count,
    matched_count,
    missing_count,
    matched_skills,
    essential_missing_skills,
    preferred_missing_skills,
    additional_skills,
    recommendations,
    suggested_career_roles,
    semantic_similarity,
    algorithm_version,
  } = analysis;

  const [downloading, setDownloading] = useState(false);

  const handleDownloadPdf = async () => {
    if (analysis.id) {
      setDownloading(true);
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/analyses/${analysis.id}/report`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        if (!response.ok) throw new Error('PDF generation failed');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `skill-gap-report-${analysis.id}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        window.print();
      } finally {
        setDownloading(false);
      }
    } else {
      window.print();
    }
  };

  return (
    <div className="container py-5">
      {/* Top Header & Actions */}
      <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3">
        <div>
          <div className="d-flex align-items-center gap-2 mb-1">
            <span className="badge bg-primary px-3 py-1 rounded-pill">
              {job_role?.category || 'Role Evaluation'}
            </span>
            <span className="badge bg-light text-muted border">
              Algorithm {algorithm_version || 'v1.0'}
            </span>
          </div>
          <h2 className="fw-bold mb-0">Analysis: {job_role?.title}</h2>
          <small className="text-muted">
            Evaluated on {new Date().toLocaleDateString()} &bull; Transparent deterministic gap audit
          </small>
        </div>

        <div className="d-flex gap-2">
          <button
            onClick={handleDownloadPdf}
            disabled={downloading}
            className="btn btn-outline-secondary rounded-pill px-3"
          >
            {downloading ? (
              <span className="spinner-border spinner-border-sm me-1" role="status"></span>
            ) : (
              <i className="bi bi-file-earmark-pdf me-1"></i>
            )}
            Download PDF Report
          </button>
          <Link to="/analyze" className="btn btn-primary rounded-pill px-3 shadow-sm">
            <i className="bi bi-arrow-repeat me-1"></i> Analyze Another
          </Link>
        </div>
      </div>

      {/* Score Overview Cards */}
      <div className="row g-4 mb-4">
        {/* Match Percentage Card */}
        <div className="col-md-4">
          <div className="card h-100 p-4 border-0 shadow-sm text-center d-flex flex-column justify-content-center">
            <span className="small text-muted fw-semibold text-uppercase tracking-wider mb-2">
              Skill Match Score
            </span>
            <div className="display-4 fw-bold text-primary mb-1">
              {match_percentage}%
            </div>
            <div className="progress mb-2" style={{ height: '8px' }}>
              <div
                className={`progress-bar ${match_percentage >= 70 ? 'bg-success' : match_percentage >= 40 ? 'bg-warning' : 'bg-danger'}`}
                role="progressbar"
                style={{ width: `${match_percentage}%` }}
              ></div>
            </div>
            <p className="small text-muted mb-0">
              {matched_count} of {total_required_count} required competencies identified
            </p>
          </div>
        </div>

        {/* Weighted Match Percentage Card */}
        <div className="col-md-4">
          <div className="card h-100 p-4 border-0 shadow-sm text-center d-flex flex-column justify-content-center">
            <span className="small text-muted fw-semibold text-uppercase tracking-wider mb-2">
              Weighted Match Score
            </span>
            <div className="display-4 fw-bold text-success mb-1">
              {weighted_match_percentage}%
            </div>
            <div className="progress mb-2" style={{ height: '8px' }}>
              <div
                className="progress-bar bg-success"
                role="progressbar"
                style={{ width: `${weighted_match_percentage}%` }}
              ></div>
            </div>
            <p className="small text-muted mb-0">
              Accounts for essential vs. preferred skill importance weights
            </p>
          </div>
        </div>

        {/* Semantic Alignment Card */}
        <div className="col-md-4">
          <div className="card h-100 p-4 border-0 shadow-sm text-center d-flex flex-column justify-content-center">
            <span className="small text-muted fw-semibold text-uppercase tracking-wider mb-2">
              Semantic Document Alignment
            </span>
            <div className="fs-3 fw-bold text-dark mb-1">
              {semantic_similarity?.interpretation || 'Evaluated'}
            </div>
            <span className="badge bg-info-subtle text-info border border-info-subtle px-3 py-1 rounded-pill mx-auto mb-2">
              {semantic_similarity?.similarity_percentage}% Cosine Similarity
            </span>
            <p className="small text-muted mb-0">
              Shared vocabulary: {semantic_similarity?.shared_keywords?.slice(0, 4).join(', ') || 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Categorized Skills Section */}
      <div className="card border-0 shadow-sm mb-5 p-4">
        <ul className="nav nav-pills mb-4 gap-2 border-bottom pb-3">
          <li className="nav-item">
            <button
              onClick={() => setActiveTab('matched')}
              className={`nav-link rounded-pill px-4 ${activeTab === 'matched' ? 'active' : ''}`}
            >
              <i className="bi bi-check-circle-fill me-1"></i> Matched ({matched_skills?.length || 0})
            </button>
          </li>
          <li className="nav-item">
            <button
              onClick={() => setActiveTab('essential')}
              className={`nav-link rounded-pill px-4 ${activeTab === 'essential' ? 'active bg-danger' : ''}`}
            >
              <i className="bi bi-exclamation-diamond-fill me-1"></i> Essential Missing ({essential_missing_skills?.length || 0})
            </button>
          </li>
          <li className="nav-item">
            <button
              onClick={() => setActiveTab('preferred')}
              className={`nav-link rounded-pill px-4 ${activeTab === 'preferred' ? 'active bg-warning text-dark' : ''}`}
            >
              <i className="bi bi-info-circle-fill me-1"></i> Preferred Missing ({preferred_missing_skills?.length || 0})
            </button>
          </li>
          <li className="nav-item">
            <button
              onClick={() => setActiveTab('additional')}
              className={`nav-link rounded-pill px-4 ${activeTab === 'additional' ? 'active bg-secondary' : ''}`}
            >
              <i className="bi bi-stars me-1"></i> Additional ({additional_skills?.length || 0})
            </button>
          </li>
        </ul>

        {/* Tab Content */}
        {activeTab === 'matched' && (
          <div>
            <p className="small text-muted mb-3">
              Skills found in your resume matching this role. Click any skill to view extracted resume sentence evidence.
            </p>
            <div className="d-flex flex-wrap gap-2">
              {matched_skills?.map((skill, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedEvidence(skill)}
                  className="btn btn-outline-success btn-sm rounded-pill px-3 py-2 text-start d-flex align-items-center gap-2"
                >
                  <i className="bi bi-check2"></i>
                  <span>{skill.name}</span>
                  <span className="badge bg-success-subtle text-success small">
                    {skill.category}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'essential' && (
          <div>
            <p className="small text-muted mb-3">
              Critical requirements for this position that were not detected in your resume. Prioritize these first.
            </p>
            <div className="d-flex flex-wrap gap-2">
              {essential_missing_skills?.map((skill, idx) => (
                <span key={idx} className="badge bg-danger-subtle text-danger border border-danger-subtle px-3 py-2 rounded-pill fs-6 fw-normal">
                  <i className="bi bi-x-circle me-1"></i> {skill.name} ({skill.category})
                </span>
              ))}
              {essential_missing_skills?.length === 0 && (
                <div className="text-success small fw-semibold">
                  <i className="bi bi-patch-check-fill me-1"></i> Great job! You matched all essential requirements!
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'preferred' && (
          <div>
            <p className="small text-muted mb-3">
              Secondary or nice-to-have tooling that provides a competitive hiring advantage.
            </p>
            <div className="d-flex flex-wrap gap-2">
              {preferred_missing_skills?.map((skill, idx) => (
                <span key={idx} className="badge bg-warning-subtle text-dark border border-warning-subtle px-3 py-2 rounded-pill fs-6 fw-normal">
                  <i className="bi bi-dash-circle me-1"></i> {skill.name} ({skill.category})
                </span>
              ))}
              {preferred_missing_skills?.length === 0 && (
                <div className="text-muted small">No preferred gaps identified.</div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'additional' && (
          <div>
            <p className="small text-muted mb-3">
              Competencies found in your resume that were not explicitly listed for this role, demonstrating extra versatility.
            </p>
            <div className="d-flex flex-wrap gap-2">
              {additional_skills?.map((skill, idx) => (
                <span key={idx} className="badge bg-light text-secondary border px-3 py-2 rounded-pill fs-6 fw-normal">
                  <i className="bi bi-gem me-1"></i> {skill.name} ({skill.category})
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Evidence Modal / Inspector */}
        {selectedEvidence && (
          <div className="alert alert-info border-0 mt-4 rounded-3 p-3">
            <div className="d-flex justify-content-between align-items-center mb-1">
              <strong className="text-info-emphasis">
                <i className="bi bi-search me-1"></i> Resume Audit Evidence for "{selectedEvidence.name}":
              </strong>
              <button
                type="button"
                className="btn-close btn-sm"
                onClick={() => setSelectedEvidence(null)}
              ></button>
            </div>
            <p className="mb-0 font-monospace small bg-white p-2 rounded border">
              "{selectedEvidence.evidence || 'Identified in technical competency profile.'}"
            </p>
          </div>
        )}
      </div>

      {/* Actionable Learning Roadmaps */}
      {recommendations && recommendations.length > 0 && (
        <div className="mb-5">
          <div className="mb-3">
            <h4 className="fw-bold mb-1">
              <i className="bi bi-journal-code text-primary me-2"></i>
              Personalized Learning Roadmaps
            </h4>
            <p className="text-muted small">
              Step-by-step topics, verified documentation links, and practice mini-projects to close your gaps.
            </p>
          </div>

          <div className="row g-4">
            {recommendations.map((rec, idx) => (
              <div key={idx} className="col-lg-6">
                <div className="card h-100 border-0 shadow-sm p-4">
                  <div className="d-flex justify-content-between align-items-start mb-2">
                    <h5 className="fw-bold mb-0 text-dark">{rec.skill_name}</h5>
                    <span
                      className={`badge px-3 py-1 rounded-pill ${
                        rec.priority === 1
                          ? 'bg-danger-subtle text-danger border border-danger-subtle'
                          : 'bg-warning-subtle text-dark border border-warning-subtle'
                      }`}
                    >
                      {rec.importance_level}
                    </span>
                  </div>

                  <p className="small text-secondary mb-3">{rec.reason}</p>

                  <h6 className="fw-semibold small text-uppercase text-muted mb-2">
                    Key Topics to Study:
                  </h6>
                  <ul className="small text-muted mb-3 ps-3">
                    {rec.recommended_topics?.map((topic, tIdx) => (
                      <li key={tIdx} className="mb-1">{topic}</li>
                    ))}
                  </ul>

                  <div className="bg-light p-3 rounded-3 small mb-3">
                    <strong className="text-primary d-block mb-1">
                      <i className="bi bi-hammer me-1"></i> Recommended Practice Exercise:
                    </strong>
                    <span className="text-muted">{rec.practice_exercise}</span>
                    <div className="text-muted small mt-2">
                      <i className="bi bi-clock me-1"></i> Estimated Time: {rec.estimated_learning_time}
                    </div>
                  </div>

                  {rec.resources && rec.resources.length > 0 && (
                    <div className="mt-auto pt-2 border-top">
                      <span className="small text-muted fw-semibold d-block mb-1">
                        Verified Learning Resources:
                      </span>
                      <div className="d-flex flex-wrap gap-2">
                        {rec.resources.map((res, rIdx) => {
                          const isYoutube =
                            res.resource_url.includes('youtube.com') ||
                            res.resource_url.includes('youtu.be') ||
                            res.title.toLowerCase().includes('youtube');
                          return (
                            <a
                              key={rIdx}
                              href={res.resource_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className={`btn btn-sm rounded-pill text-decoration-none ${
                                isYoutube ? 'btn-outline-danger' : 'btn-outline-primary'
                              }`}
                            >
                              <i
                                className={`bi ${
                                  isYoutube ? 'bi-youtube text-danger' : 'bi-box-arrow-up-right'
                                } me-1`}
                              ></i>
                              {res.title}
                            </a>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Resume Optimization & Diagnostic Advisory */}
      {(missing_count > 0 || match_percentage < 80) && (
        <div className="card border-0 shadow-sm mb-5 p-4 bg-light-subtle border-start border-4 border-warning">
          <div className="d-flex align-items-center mb-3">
            <span className="badge bg-warning text-dark me-2 px-3 py-2 rounded-pill">
              <i className="bi bi-lightbulb-fill me-1"></i> AI Resume Diagnostic
            </span>
            <h4 className="fw-bold mb-0 text-dark">
              Why Your Resume Isn't Fully Aligning & How to Fix It
            </h4>
          </div>

          <p className="text-secondary small mb-4">
            Our analysis identified specific gaps between your current resume content and what recruiters for <strong>{job_role?.title || 'this role'}</strong> expect. Here is targeted guidance on how to strengthen your resume to pass automated ATS filters and catch recruiters' attention.
          </p>

          <div className="row g-4 mb-4">
            {/* Specific Issues Identified */}
            <div className="col-md-6">
              <div className="card h-100 border-0 bg-white p-3 shadow-sm rounded-3">
                <h6 className="fw-bold text-danger mb-2">
                  <i className="bi bi-exclamation-triangle-fill me-2"></i>
                  Specific Issues Identified
                </h6>
                <ul className="small text-muted mb-0 ps-3">
                  {essential_missing_skills && essential_missing_skills.length > 0 && (
                    <li className="mb-2">
                      <strong>Missing Core Essential Competencies:</strong> Your resume lacks evidence for core requirements like{' '}
                      <span className="text-danger fw-semibold">
                        {essential_missing_skills.map((s) => s.name).join(', ')}
                      </span>
                      . Automated ATS filters will deprioritize applications missing these prerequisites.
                    </li>
                  )}
                  {semantic_similarity?.similarity_percentage < 35 && (
                    <li className="mb-2">
                      <strong>Low Industry Keyword Density:</strong> Semantic vocabulary match is at{' '}
                      <span className="fw-semibold">{semantic_similarity?.similarity_percentage}%</span>. The technical phrasing in your project descriptions diverges from standard market job descriptions.
                    </li>
                  )}
                  <li className="mb-2">
                    <strong>Absence of Production & Deployment Tooling:</strong> Modern hiring managers look for full software lifecycle evidence (containerization, automated testing, CI/CD, or cloud deployments) beyond isolated coding exercises.
                  </li>
                  <li>
                    <strong>Unquantified Project Impact:</strong> Bullet points that state tasks (e.g. <em>"worked on database"</em>) rather than outcomes fail to signal engineering competence.
                  </li>
                </ul>
              </div>
            </div>

            {/* Concrete Guidance & Details to Add */}
            <div className="col-md-6">
              <div className="card h-100 border-0 bg-white p-3 shadow-sm rounded-3">
                <h6 className="fw-bold text-success mb-2">
                  <i className="bi bi-check-circle-fill me-2"></i>
                  How to Improve Your Resume
                </h6>
                <ul className="small text-muted mb-0 ps-3">
                  <li className="mb-2">
                    <strong>Add Missing Skills to Your Technical Skills Matrix:</strong> Explicitly add missing technologies once practiced:{' '}
                    <span className="badge bg-primary-subtle text-primary me-1">
                      {(essential_missing_skills || []).map((s) => s.name).slice(0, 3).join(', ') || 'Docker, SQL, Git'}
                    </span>
                  </li>
                  <li className="mb-2">
                    <strong>Adopt Google's XYZ Bullet Formula:</strong> Reformat project bullets to: <em>"Accomplished [X], as measured by [Y], by doing [Z]"</em> (e.g., <em>"Engineered a scalable REST API in Python handling 500+ daily requests by implementing MySQL indexing and connection pooling."</em>)
                  </li>
                  <li className="mb-2">
                    <strong>Include 2 Hands-On Capstone Projects:</strong> Build and link GitHub repositories that specifically showcase the missing skills (e.g., containerized full-stack apps with automated pytest unit tests).
                  </li>
                  <li>
                    <strong>Add Architecture Details:</strong> Specify database schemas, API authentication protocols (JWT, OAuth), and deployment environments (Docker, AWS) in your project descriptions.
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Curated YouTube Video Guides */}
          <div className="bg-white p-3 rounded-3 shadow-sm">
            <h6 className="fw-bold text-dark mb-2">
              <i className="bi bi-youtube text-danger me-2"></i>
              Recommended Masterclasses & Video Tutorials
            </h6>
            <div className="row g-3">
              <div className="col-lg-4">
                <a
                  href="https://www.youtube.com/watch?v=y3U_0uS5WkQ"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="card h-100 border text-decoration-none p-3 shadow-sm"
                >
                  <div className="d-flex align-items-center mb-1">
                    <i className="bi bi-play-circle-fill text-danger fs-4 me-2"></i>
                    <strong className="text-dark small">How to Write a Tech Resume that Gets Interviews</strong>
                  </div>
                  <span className="text-muted small">freeCodeCamp • ATS-friendly structure & project descriptions</span>
                </a>
              </div>

              <div className="col-lg-4">
                <a
                  href="https://www.youtube.com/watch?v=xpzp6s_J8tI"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="card h-100 border text-decoration-none p-3 shadow-sm"
                >
                  <div className="d-flex align-items-center mb-1">
                    <i className="bi bi-play-circle-fill text-danger fs-4 me-2"></i>
                    <strong className="text-dark small">Software Engineer Resume Teardown & Review</strong>
                  </div>
                  <span className="text-muted small">Tech With Tim • Live critique of strong vs weak candidate resumes</span>
                </a>
              </div>

              <div className="col-lg-4">
                <a
                  href="https://www.youtube.com/watch?v=SLwpqD8n3d0"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="card h-100 border text-decoration-none p-3 shadow-sm"
                >
                  <div className="d-flex align-items-center mb-1">
                    <i className="bi bi-play-circle-fill text-danger fs-4 me-2"></i>
                    <strong className="text-dark small">Full Stack System Architecture & REST APIs</strong>
                  </div>
                  <span className="text-muted small">Traversy Media • Essential architectural concepts recruiters probe</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Alternative Career Paths */}
      {suggested_career_roles && suggested_career_roles.length > 0 && (
        <div className="mb-5">
          <div className="mb-3">
            <h4 className="fw-bold mb-1">
              <i className="bi bi-compass text-primary me-2"></i>
              Alternative Career Role Opportunities
            </h4>
            <p className="text-muted small">
              Based on your demonstrated competencies, you also show strong overlap for these industry positions.
            </p>
          </div>

          <div className="row g-4">
            {suggested_career_roles.map((career, idx) => (
              <div key={idx} className="col-md-4">
                <div className="card h-100 border-0 shadow-sm p-4">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="badge bg-secondary-subtle text-secondary rounded-pill px-2 py-1">
                      {career.category}
                    </span>
                    <span className="badge bg-success-subtle text-success fs-6 fw-bold px-2 py-1 rounded-pill">
                      {career.match_percentage}% Match
                    </span>
                  </div>
                  <h5 className="fw-bold mb-2 text-dark">{career.title}</h5>
                  <p className="small text-muted mb-3">
                    {career.recommendation_reason}
                  </p>
                  <div className="small text-muted mt-auto pt-2 border-top">
                    <i className="bi bi-info-circle me-1"></i>
                    {career.disclaimer}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Results;

