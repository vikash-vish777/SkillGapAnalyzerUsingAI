import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark app-navbar py-3">
      <div className="container">
        <Link className="navbar-brand fw-bold d-flex align-items-center gap-2" to="/">
          <i className="bi bi-cpu-fill text-primary fs-3"></i>
          <span className="fs-4 tracking-tight">SkillGap AI</span>
        </Link>
        <button
          className="navbar-toggler border-0"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto align-items-center gap-2 mt-3 mt-lg-0">
            <li className="nav-item">
              <Link className="nav-link px-3" to="/">Home</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link px-3 fw-semibold text-primary" to="/analyze">
                <i className="bi bi-file-earmark-arrow-up me-1"></i> Analyze Resume
              </Link>
            </li>

            {isAuthenticated ? (
              <>
                <li className="nav-item">
                  <Link className="nav-link px-3" to="/dashboard">
                    <i className="bi bi-speedometer2 me-1"></i> Dashboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link px-3" to="/history">
                    <i className="bi bi-clock-history me-1"></i> History
                  </Link>
                </li>
                <li className="nav-item dropdown">
                  <div className="d-flex align-items-center gap-2 ms-lg-2">
                    <span className="badge bg-secondary-subtle text-light border border-secondary px-3 py-2 rounded-pill">
                      <i className="bi bi-person-circle me-1"></i> {user?.full_name?.split(' ')[0] || 'Account'}
                    </span>
                    <button
                      onClick={handleLogout}
                      className="btn btn-outline-danger btn-sm px-3 rounded-pill"
                      title="Log Out"
                    >
                      <i className="bi bi-box-arrow-right me-1"></i> Logout
                    </button>
                  </div>
                </li>
              </>
            ) : (
              <>
                <li className="nav-item ms-lg-2">
                  <Link className="btn btn-outline-light btn-sm px-3 rounded-pill" to="/login">
                    Sign In
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="btn btn-primary btn-sm px-3 rounded-pill shadow-sm" to="/register">
                    Create Account
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
