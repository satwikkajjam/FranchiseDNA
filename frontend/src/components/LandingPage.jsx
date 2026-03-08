import React from 'react';
import Logo from './Logo';

function LandingPage({ onEnter }) {
  return (
    <div className="landing">
      <div className="bubbles">
        {Array.from({ length: 12 }).map((_, i) => (
          <span key={i} className="bubble" />
        ))}
      </div>

      <div className="landing-hero">
        <div className="landing-logo">
          <Logo size={56} light />
          <h1>FranchiseDNA</h1>
        </div>
        <p className="landing-tagline">
          Franchise Location Intelligence
        </p>
        <p className="landing-sub">
          Analyze demographics, detect competitors, predict profits and assess risk
          across India — powered by Census 2011 data and real-time intelligence.
        </p>
        <button className="landing-cta" onClick={onEnter}>
          Launch Platform
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <line x1="5" y1="12" x2="19" y2="12" />
            <polyline points="12 5 19 12 12 19" />
          </svg>
        </button>
      </div>

      <div className="landing-features">
        <div className="feature-card">
          <div className="feature-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
          </div>
          <h3>Population Analysis</h3>
          <p>Deep demographic insights from Census 2011 covering 640+ districts and household data.</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" /><circle cx="12" cy="10" r="3" />
            </svg>
          </div>
          <h3>Competitor Detection</h3>
          <p>Discover nearby competitors via Google Places and OpenStreetMap in real-time.</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="1" x2="12" y2="23" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
            </svg>
          </div>
          <h3>Profit Prediction</h3>
          <p>Revenue forecasting with 5-year projections, break-even and ROI analysis.</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
          </div>
          <h3>Risk Assessment</h3>
          <p>Multi-factor risk scoring across competition, density, investment and profitability.</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2" /><line x1="8" y1="21" x2="16" y2="21" /><line x1="12" y1="17" x2="12" y2="21" />
            </svg>
          </div>
          <h3>90 Store Types</h3>
          <p>From Coffee Shops to Drone Stores — find the perfect franchise for any locality.</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" />
            </svg>
          </div>
          <h3>PDF Reports</h3>
          <p>Download comprehensive reports with charts, tables and actionable insights.</p>
        </div>
      </div>

      <footer className="landing-footer">
        <p>Census 2011 &middot; Google Places &middot; OpenStreetMap</p>
        <p className="footer-copyright">&copy; 2026 FranchiseDNA. Built by Sathwik Kajjam. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default LandingPage;
