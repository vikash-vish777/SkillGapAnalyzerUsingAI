import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const Home = () => {
  const [backendHealth, setBackendHealth] = useState({
    status: 'checking',
    message: 'Testing connection to Flask backend...',
    data: null,
  });

  useEffect(() => {
    // Ping backend health check on mount
    api.get('/health')
      .then((res) => {
        setBackendHealth({
          status: 'online',
          message: 'Backend is connected and healthy',
          data: res.data,
        });
      })
      .catch((err) => {
        setBackendHealth({
          status: 'offline',
          message: err.message,
          data: null,
        });
      });
  }, []);

  return (
    <div className="container py-5">
      {/* Hero Section */}
      <div className="row align-items-center mb-5">
        <div className="col-lg-7">
          <span className="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 rounded-pill mb-3">
            <i className="bi bi-stars me-1"></i> AI-Powered Career Intelligence
          </span>
          <h1 className="display-4 fw-bold mb-3 text-dark">
            Discover Your Tech Skill Gaps with Precision AI
          </h1>
          <p className="lead text-secondary mb-4">
            Upload your resume, benchmark against real-world job roles, uncover missing technical skills, and follow personalized learning roadmaps designed for career growth.
          </p>
          <div className="d-flex flex-wrap gap-3">
            <Link to="/register" className="btn btn-primary btn-lg px-4 shadow-sm">
              <i className="bi bi-rocket-takeoff me-2"></i> Get Started Free
            </Link>
            <Link to="/login" className="btn btn-outline-secondary btn-lg px-4">
              Sign In
            </Link>
          </div>
        </div>

        {/* Backend Status Card */}
        <div className="col-lg-5 mt-4 mt-lg-0">
          <div className="card shadow-sm border-0 p-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0 fw-semibold">System Status</h5>
              {backendHealth.status === 'online' && (
                <span className="badge bg-success-subtle text-success border border-success-subtle px-2 py-1">
                  <i className="bi bi-circle-fill me-1 small"></i> API Online
                </span>
              )}
              {backendHealth.status === 'checking' && (
                <span className="badge bg-warning-subtle text-warning border border-warning-subtle px-2 py-1">
                  <i className="bi bi-hourglass-split me-1"></i> Checking API
                </span>
              )}
              {backendHealth.status === 'offline' && (
                <span className="badge bg-danger-subtle text-danger border border-danger-subtle px-2 py-1">
                  <i className="bi bi-exclamation-triangle-fill me-1"></i> API Offline
                </span>
              )}
            </div>

            <p className="small text-muted mb-3">{backendHealth.message}</p>

            {backendHealth.data && (
              <div className="bg-light p-3 rounded small font-monospace">
                <div><strong>Backend:</strong> Flask {backendHealth.data.version}</div>
                <div><strong>Status:</strong> {backendHealth.data.status}</div>
                <div><strong>Database:</strong> {backendHealth.data.database}</div>
              </div>
            )}

            <div className="mt-4 pt-3 border-top small text-muted">
              <i className="bi bi-info-circle me-1"></i> Full-stack communication established via REST API.
            </div>
          </div>
        </div>
      </div>

      {/* Feature Highlights */}
      <div className="row g-4 mt-2">
        <div className="col-md-4">
          <div className="card h-100 p-4">
            <div className="fs-1 text-primary mb-3">
              <i className="bi bi-file-earmark-text"></i>
            </div>
            <h5 className="fw-bold">Intelligent Resume Parsing</h5>
            <p className="text-secondary small mb-0">
              High-fidelity text extraction from PDF and DOCX formats without storing private documents on disk.
            </p>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card h-100 p-4">
            <div className="fs-1 text-primary mb-3">
              <i className="bi bi-diagram-3"></i>
            </div>
            <h5 className="fw-bold">Hybrid NLP Extraction</h5>
            <p className="text-secondary small mb-0">
              Combines canonical dictionaries, regex word-boundaries, and semantic embeddings to avoid false positives.
            </p>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card h-100 p-4">
            <div className="fs-1 text-primary mb-3">
              <i className="bi bi-bullseye"></i>
            </div>
            <h5 className="fw-bold">Transparent Scoring</h5>
            <p className="text-secondary small mb-0">
              Clear, weighted match metrics that clearly distinguish essential requirements from preferred skills.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

