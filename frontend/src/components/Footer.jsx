import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-white border-top py-4 mt-auto">
      <div className="container text-center text-muted small">
        <p className="mb-1">
          <strong>Skill Gap Analyzer Using Artificial Intelligence (AI)</strong> &copy; {new Date().getFullYear()}
        </p>
        <p className="mb-0">
          Built with React, Flask, and spaCy NLP. Empowering candidates with actionable career insights.
        </p>
      </div>
    </footer>
  );
};

export default Footer;

