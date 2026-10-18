import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Register = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrorMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.fullName.trim()) {
      setErrorMessage('Please enter your full name.');
      return;
    }
    if (!formData.email.trim()) {
      setErrorMessage('Please enter a valid email address.');
      return;
    }
    if (formData.password.length < 8) {
      setErrorMessage('Password must be at least 8 characters long.');
      return;
    }
    if (formData.password !== formData.confirmPassword) {
      setErrorMessage('Passwords do not match.');
      return;
    }

    setLoading(true);
    const result = await register(formData.fullName, formData.email, formData.password);
    setLoading(false);

    if (result.success) {
      navigate('/dashboard');
    } else {
      setErrorMessage(result.message || 'Registration failed. Please try again.');
    }
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-7 col-lg-5">
          <div className="card shadow-sm border-0 p-4 p-md-5">
            <div className="text-center mb-4">
              <div className="display-6 text-primary mb-2">
                <i className="bi bi-person-plus-fill"></i>
              </div>
              <h3 className="fw-bold text-dark">Create Account</h3>
              <p className="text-muted small">
                Join SkillGap AI to benchmark your skills against industry standards
              </p>
            </div>

            {errorMessage && (
              <div className="alert alert-danger d-flex align-items-center gap-2 small py-2" role="alert">
                <i className="bi bi-exclamation-octagon-fill"></i>
                <div>{errorMessage}</div>
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label small fw-semibold">Full Name</label>
                <div className="input-group">
                  <span className="input-group-text bg-light text-muted border-end-0">
                    <i className="bi bi-person"></i>
                  </span>
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleChange}
                    className="form-control border-start-0"
                    placeholder="Jane Doe"
                    required
                  />
                </div>
              </div>

              <div className="mb-3">
                <label className="form-label small fw-semibold">Email Address</label>
                <div className="input-group">
                  <span className="input-group-text bg-light text-muted border-end-0">
                    <i className="bi bi-envelope"></i>
                  </span>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="form-control border-start-0"
                    placeholder="jane@example.com"
                    required
                  />
                </div>
              </div>

              <div className="mb-3">
                <label className="form-label small fw-semibold">Password</label>
                <div className="input-group">
                  <span className="input-group-text bg-light text-muted border-end-0">
                    <i className="bi bi-shield-lock"></i>
                  </span>
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="form-control border-start-0"
                    placeholder="Minimum 8 characters"
                    required
                  />
                </div>
              </div>

              <div className="mb-4">
                <label className="form-label small fw-semibold">Confirm Password</label>
                <div className="input-group">
                  <span className="input-group-text bg-light text-muted border-end-0">
                    <i className="bi bi-shield-check"></i>
                  </span>
                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className="form-control border-start-0"
                    placeholder="Re-enter password"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary w-100 py-2 fw-semibold shadow-sm rounded-pill"
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Creating Account...
                  </>
                ) : (
                  'Create Account'
                )}
              </button>
            </form>

            <div className="text-center mt-4 pt-3 border-top small text-muted">
              Already have an account?{' '}
              <Link to="/login" className="text-primary fw-semibold text-decoration-none">
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;

