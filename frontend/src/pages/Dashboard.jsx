import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

const Dashboard = () => {
  const { user } = useAuth();
  const [metrics, setMetrics] = useState({
    total_analyses: 0,
    latest_match_percentage: null,
    average_match_percentage: null,
    recent_analyses: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/users/dashboard')
      .then((res) => {
        if (res.success && res.data) {
          setMetrics(res.data);
        }
      })
      .catch((err) => {
        console.error('Failed to load dashboard metrics:', err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="container py-5">
      {/* Header Greeting */}
      <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3">
        <div>
          <h2 className="fw-bold mb-1">
            Welcome, {user?.full_name || 'Candidate'}! 👋
          </h2>
          <p className="text-muted mb-0 small">
            Here is a summary of your career benchmarking and skill analytics.
          </p>
        </div>
        <Link to="/analyze" className="btn btn-primary px-4 py-2 rounded-pill shadow-sm">
          <i className="bi bi-plus-lg me-2"></i> New Resume Analysis
        </Link>
      </div>

      {/* Metrics Row */}
      <div className="row g-4 mb-5">
        <div className="col-sm-6 col-lg-4">
          <div className="card h-100 p-4 border-0 shadow-sm">
            <div className="d-flex justify-content-between align-items-center mb-2">
              <span className="text-muted small fw-semibold text-uppercase tracking-wider">
                Total Analyses
              </span>
              <span className="badge bg-primary-subtle text-primary p-2 rounded-3">
                <i className="bi bi-file-earmark-check fs-5"></i>
              </span>
            </div>
            <h2 className="display-6 fw-bold mb-0 text-dark">
              {metrics.total_analyses}
            </h2>
            <div className="small text-muted mt-2">
              Resumes benchmarked against industry roles
            </div>
          </div>
        </div>

        <div className="col-sm-6 col-lg-4">
          <div className="card h-100 p-4 border-0 shadow-sm">
            <div className="d-flex justify-content-between align-items-center mb-2">
              <span className="text-muted small fw-semibold text-uppercase tracking-wider">
                Latest Match Score
              </span>
              <span className="badge bg-success-subtle text-success p-2 rounded-3">
                <i className="bi bi-award fs-5"></i>
              </span>
            </div>
            <h2 className="display-6 fw-bold mb-0 text-dark">
              {metrics.latest_match_percentage !== null
                ? `${metrics.latest_match_percentage}%`
                : 'N/A'}
            </h2>
            <div className="small text-muted mt-2">
              {metrics.latest_match_percentage !== null
                ? 'Score from your most recent analysis'
                : 'No analysis run yet'}
            </div>
          </div>
        </div>

        <div className="col-sm-6 col-lg-4">
          <div className="card h-100 p-4 border-0 shadow-sm">
            <div className="d-flex justify-content-between align-items-center mb-2">
              <span className="text-muted small fw-semibold text-uppercase tracking-wider">
                Average Match
              </span>
              <span className="badge bg-info-subtle text-info p-2 rounded-3">
                <i className="bi bi-graph-up-arrow fs-5"></i>
              </span>
            </div>
            <h2 className="display-6 fw-bold mb-0 text-dark">
              {metrics.average_match_percentage !== null
                ? `${metrics.average_match_percentage}%`
                : 'N/A'}
            </h2>
            <div className="small text-muted mt-2">
              Overall competency alignment average
            </div>
          </div>
        </div>
      </div>

      {/* Main Action Banner */}
      <div className="card bg-primary text-white border-0 p-4 p-md-5 mb-5 rounded-4 shadow-sm">
        <div className="row align-items-center">
          <div className="col-lg-8">
            <span className="badge bg-white text-primary px-3 py-1 rounded-pill fw-semibold mb-3">
              Precision AI Gap Engine v1.0
            </span>
            <h3 className="fw-bold mb-2">Ready to audit your resume for a dream role?</h3>
            <p className="lead mb-3 text-white-50 small">
              Upload your PDF or Word resume, select your target position, and uncover essential vs. preferred skill gaps with verified learning resources.
            </p>
          </div>
          <div className="col-lg-4 text-lg-end mt-3 mt-lg-0">
            <Link to="/analyze" className="btn btn-light btn-lg px-4 py-3 rounded-pill fw-bold text-primary shadow">
              <i className="bi bi-lightning-charge-fill me-2"></i> Run Analysis Now
            </Link>
          </div>
        </div>
      </div>

      {/* Recent History Table */}
      <div className="card border-0 shadow-sm p-4">
        <h5 className="fw-bold mb-3">Recent Analyses</h5>
        {metrics.recent_analyses && metrics.recent_analyses.length > 0 ? (
          <div className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead className="table-light small text-uppercase text-muted">
                <tr>
                  <th>Job Role</th>
                  <th>Match Score</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {metrics.recent_analyses.map((item) => (
                  <tr key={item.id}>
                    <td className="fw-semibold">{item.job_role_title || 'Custom Role'}</td>
                    <td>
                      <span className="badge bg-success-subtle text-success px-2 py-1 rounded-pill">
                        {item.match_percentage}%
                      </span>
                    </td>
                    <td>
                      <span className="badge bg-light text-dark border">
                        {item.analysis_status}
                      </span>
                    </td>
                    <td className="small text-muted">
                      {new Date(item.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-5 text-muted">
            <i className="bi bi-clipboard-data fs-1 d-block mb-2 text-secondary"></i>
            <p className="mb-2">No historical analyses recorded yet.</p>
            <Link to="/analyze" className="btn btn-outline-primary btn-sm rounded-pill px-3">
              Analyze your first resume
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

