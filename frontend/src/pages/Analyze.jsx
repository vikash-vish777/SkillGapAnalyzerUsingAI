import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const Analyze = () => {
  const [jobRoles, setJobRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState('');
  const [customJd, setCustomJd] = useState('');
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');

  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  // Load available job roles on mount
  useEffect(() => {
    api.get('/job-roles')
      .then((res) => {
        if (res.success && res.data) {
          setJobRoles(res.data);
          if (res.data.length > 0) {
            setSelectedRole(res.data[0].id.toString());
          }
        }
      })
      .catch((err) => {
        console.error('Failed to load job roles:', err);
      });
  }, []);

  const handleFileDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    setErrorMessage('');
    const lowerName = selectedFile.name.toLowerCase();
    if (!lowerName.endsWith('.pdf') && !lowerName.endsWith('.docx')) {
      setErrorMessage('Unsupported file format. Please upload a PDF (.pdf) or Word (.docx) document.');
      return;
    }
    if (selectedFile.size > 5 * 1024 * 1024) {
      setErrorMessage('File size exceeds the 5 MB limit. Please upload a smaller file.');
      return;
    }
    setFile(selectedFile);
  };

  const handleRemoveFile = () => {
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setErrorMessage('Please select a resume file to upload.');
      return;
    }
    if (!selectedRole) {
      setErrorMessage('Please choose a target job role.');
      return;
    }

    setLoading(true);
    setErrorMessage('');

    // Dynamic progressive feedback simulation
    setLoadingStep('Uploading & inspecting document security signatures...');
    setTimeout(() => setLoadingStep('Extracting skills using hybrid regex & NLP...'), 700);
    setTimeout(() => setLoadingStep('Benchmarking competencies & calculating gap metrics...'), 1400);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_role_id', selectedRole);
    if (customJd.trim()) {
      formData.append('custom_job_description', customJd.trim());
    }

    try {
      const response = await api.post('/analyses', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (response.success && response.data) {
        // Persist analysis in session storage and navigate to results view
        sessionStorage.setItem('current_analysis', JSON.stringify(response.data));
        navigate('/results', { state: { analysis: response.data } });
      } else {
        setErrorMessage(response.message || 'Analysis could not be completed.');
      }
    } catch (err) {
      setErrorMessage(err.message || 'An error occurred during resume processing.');
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-9 col-xl-8">
          <div className="card shadow-sm border-0 p-4 p-md-5">
            <div className="text-center mb-4">
              <span className="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-1 rounded-pill mb-2">
                <i className="bi bi-cpu-fill me-1"></i> NLP Skill Extraction Engine
              </span>
              <h2 className="fw-bold">Analyze Your Resume</h2>
              <p className="text-muted small">
                Upload your resume, select your target role, and discover your personalized gap analysis.
              </p>
            </div>

            {errorMessage && (
              <div className="alert alert-danger d-flex align-items-center gap-2 small py-2 mb-4" role="alert">
                <i className="bi bi-exclamation-octagon-fill fs-5"></i>
                <div>{errorMessage}</div>
              </div>
            )}

            <form onSubmit={handleSubmit}>
              {/* Dropzone Upload */}
              <div className="mb-4">
                <label className="form-label fw-semibold small text-uppercase text-muted">
                  1. Resume Document (PDF or DOCX)
                </label>

                {!file ? (
                  <div
                    onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                    onDragLeave={() => setIsDragging(false)}
                    onDrop={handleFileDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className={`border border-2 border-dashed rounded-4 p-5 text-center cursor-pointer transition ${
                      isDragging ? 'border-primary bg-primary-subtle' : 'border-secondary-subtle bg-light'
                    }`}
                    style={{ cursor: 'pointer' }}
                  >
                    <i className="bi bi-cloud-arrow-up display-4 text-primary mb-3 d-block"></i>
                    <h6 className="fw-bold mb-1">Drag and drop your resume here, or browse</h6>
                    <p className="text-muted small mb-0">
                      Supports PDF and Word DOCX formats (Up to 5 MB)
                    </p>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                      onChange={handleFileSelect}
                      className="d-none"
                    />
                  </div>
                ) : (
                  <div className="border rounded-4 p-3 bg-light d-flex align-items-center justify-content-between">
                    <div className="d-flex align-items-center gap-3">
                      <div className="p-3 bg-white rounded-3 shadow-sm text-primary fs-3">
                        <i className={file.name.toLowerCase().endsWith('.pdf') ? 'bi bi-file-earmark-pdf' : 'bi bi-file-earmark-word'}></i>
                      </div>
                      <div>
                        <h6 className="mb-0 fw-semibold">{file.name}</h6>
                        <span className="text-muted small">
                          {(file.size / 1024).toFixed(1)} KB &bull; Ready for AI extraction
                        </span>
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={handleRemoveFile}
                      className="btn btn-outline-danger btn-sm rounded-pill px-3"
                    >
                      <i className="bi bi-x-lg me-1"></i> Replace
                    </button>
                  </div>
                )}
              </div>

              {/* Target Job Role */}
              <div className="mb-4">
                <label className="form-label fw-semibold small text-uppercase text-muted">
                  2. Select Target Job Role
                </label>
                <select
                  className="form-select py-2 border-secondary-subtle"
                  value={selectedRole}
                  onChange={(e) => setSelectedRole(e.target.value)}
                  required
                >
                  {jobRoles.map((role) => (
                    <option key={role.id} value={role.id}>
                      {role.title} ({role.category})
                    </option>
                  ))}
                </select>
                <div className="form-text small">
                  The system will benchmark your skills against verified competency requirements for this role.
                </div>
              </div>

              {/* Optional Custom Job Description */}
              <div className="mb-4">
                <div className="d-flex justify-content-between align-items-center mb-1">
                  <label className="form-label fw-semibold small text-uppercase text-muted mb-0">
                    3. Optional: Custom Job Description
                  </label>
                  <span className="badge bg-light text-muted border">Optional</span>
                </div>
                <textarea
                  className="form-control border-secondary-subtle"
                  rows={3}
                  placeholder="Paste specific job requirements or job posting text here to extract dynamic skills and compute semantic similarity..."
                  value={customJd}
                  onChange={(e) => setCustomJd(e.target.value)}
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading || !file}
                className="btn btn-primary w-100 py-3 fw-bold rounded-pill shadow-sm"
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {loadingStep || 'Processing Resume...'}
                  </>
                ) : (
                  <>
                    <i className="bi bi-magic me-2"></i> Run AI Skill Gap Analysis
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analyze;

