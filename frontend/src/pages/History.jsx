import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const History = () => {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloadingId, setDownloadingId] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    loadAnalyses();
  }, [isAuthenticated, navigate]);

  const loadAnalyses = () => {
    setLoading(true);
    api.get('/analyses')
      .then((res) => {
        if (res.success && res.data) {
          setAnalyses(res.data);
        }
      })
      .catch((err) => {
        setErrorMessage(err.message || 'Failed to load analysis history.');
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handleViewDetail = async (id) => {
    try {
      const res = await api.get(`/analyses/${id}`);
      if (res.success && res.data) {
        sessionStorage.setItem('current_analysis', JSON.stringify(res.data));
        navigate('/results', { state: { analysis: res.data } });
      }
    } catch (err) {
      alert(err.message || 'Failed to open past analysis report.');
    }
  };

  const handleDownloadPdf = async (id) => {
    setDownloadingId(id);
    try {
      // Direct raw fetch with auth header for blob download
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/analyses/${id}/report`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to download PDF report.');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `skill-gap-report-${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert(err.message || 'Error downloading PDF.');
    } finally {
      setDownloadingId(null);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this historical analysis?')) {
      return;
    }

    try {
      await api.delete(`/analyses/${id}`);
      setAnalyses(analyses.filter((a) => a.id !== id));
    } catch (err) {
      alert(err.message || 'Failed to delete analysis record.');
    }
  };

  return (
    <div className="container py-5">
      <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3">
        <div>
          <h2 className="fw-bold mb-1">Analysis History</h2>
          <p className="text-muted small mb-0">
            Review past skill gap evaluations, download official PDF reports, or track growth over time.
          </p>
        </div>
        <Link to="/analyze" className="btn btn-primary rounded-pill px-4 shadow-sm">
          <i className="bi bi-plus-lg me-1"></i> New Analysis
        </Link>
      </div>

      {errorMessage && (
        <div className="alert alert-danger small py-2 mb-4" role="alert">
          {errorMessage}
        </div>
      )}

      {loading ? (
        <div className="card border-0 shadow-sm p-5 text-center">
          <div className="spinner-border text-primary mx-auto mb-3" role="status"></div>
          <span className="text-muted small">Loading your saved analysis records...</span>
        </div>
      ) : analyses.length > 0 ? (
        <div className="card border-0 shadow-sm p-0 overflow-hidden">
          <div className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead className="table-light small text-uppercase text-muted">
                <tr>
                  <th className="ps-4">Analysis ID</th>
                  <th>Target Job Role</th>
                  <th>Match Score</th>
                  <th>Weighted Score</th>
                  <th>Date Evaluated</th>
                  <th className="text-end pe-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                {analyses.map((item) => (
                  <tr key={item.id}>
                    <td className="ps-4 font-monospace fw-semibold">
                      #{item.id}
                    </td>
                    <td>
                      <span className="fw-bold text-dark d-block">
                        {item.job_role_title || 'Custom Evaluation'}
                      </span>
                      <small className="text-muted">Algorithm {item.algorithm_version}</small>
                    </td>
                    <td>
                      <span className="badge bg-primary-subtle text-primary fs-6 px-3 py-1 rounded-pill">
                        {item.match_percentage}%
                      </span>
                    </td>
                    <td>
                      <span className="badge bg-success-subtle text-success fs-6 px-3 py-1 rounded-pill">
                        {item.weighted_match_percentage}%
                      </span>
                    </td>
                    <td className="small text-muted">
                      {new Date(item.created_at).toLocaleDateString()} &bull;{' '}
                      {new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </td>
                    <td className="text-end pe-4">
                      <div className="btn-group">
                        <button
                          onClick={() => handleViewDetail(item.id)}
                          className="btn btn-outline-primary btn-sm rounded-pill px-3 me-1"
                          title="Open Interactive Results"
                        >
                          <i className="bi bi-eye me-1"></i> View
                        </button>
                        <button
                          onClick={() => handleDownloadPdf(item.id)}
                          disabled={downloadingId === item.id}
                          className="btn btn-outline-secondary btn-sm rounded-pill px-3 me-1"
                          title="Download Official PDF Report"
                        >
                          {downloadingId === item.id ? (
                            <span className="spinner-border spinner-border-sm" role="status"></span>
                          ) : (
                            <>
                              <i className="bi bi-file-earmark-pdf me-1"></i> PDF
                            </>
                          )}
                        </button>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="btn btn-outline-danger btn-sm rounded-pill px-2"
                          title="Delete Record"
                        >
                          <i className="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="card border-0 shadow-sm p-5 text-center">
          <i className="bi bi-archive display-4 text-muted mb-3"></i>
          <h5 className="fw-bold">No Past Analyses Found</h5>
          <p className="text-muted small mb-3">
            You haven't run any resume skill audits under this account yet.
          </p>
          <div>
            <Link to="/analyze" className="btn btn-primary rounded-pill px-4">
              <i className="bi bi-rocket-takeoff me-1"></i> Analyze Your First Resume
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
