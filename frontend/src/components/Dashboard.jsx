import React from 'react';
import PopulationStats from './PopulationStats';
import CompetitorPanel from './CompetitorPanel';
import ProfitPrediction from './ProfitPrediction';
import RiskAnalysis from './RiskAnalysis';
import RecommendationPanel from './RecommendationPanel';

function Dashboard({ data, onBack, onDownloadPdf }) {
  if (!data) return null;

  return (
    <div className="dashboard">
      <div className="bubbles">
        {Array.from({ length: 12 }).map((_, i) => (
          <span key={i} className="bubble" />
        ))}
      </div>

      <div className="dashboard-header">
        <div>
          <h2>Analysis</h2>
          <div className="location-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            {data.location.name} &middot; {data.location.radius_km} km
          </div>
        </div>
        <div className="dashboard-actions">
          <button className="btn-back" onClick={onBack}>Back</button>
          <button className="btn-pdf" onClick={onDownloadPdf}>Export PDF</button>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <div className="card-header">
            <div className="card-header-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            </div>
            <h3>Population</h3>
          </div>
          <div className="card-body">
            <PopulationStats data={data.population} />
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-header">
            <div className="card-header-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            </div>
            <h3>Risk</h3>
          </div>
          <div className="card-body">
            <RiskAnalysis data={data.risk} />
          </div>
        </div>

        <div className="dashboard-card full-width">
          <div className="card-header">
            <div className="card-header-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            </div>
            <h3>Profit & Projections</h3>
          </div>
          <div className="card-body">
            <ProfitPrediction profitData={data.profit} projections={data.projections} />
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-header">
            <div className="card-header-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            </div>
            <h3>Competitors</h3>
          </div>
          <div className="card-body">
            <CompetitorPanel data={data.competitors} />
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-header">
            <div className="card-header-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <h3>Recommendations</h3>
          </div>
          <div className="card-body">
            <RecommendationPanel recommendations={data.recommendations} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
