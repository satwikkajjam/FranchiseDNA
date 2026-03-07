import React from 'react';

function formatCurrency(amount) {
  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(2)} Cr`;
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(2)} L`;
  return `₹${Math.round(amount).toLocaleString()}`;
}

function RecommendationPanel({ recommendations }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="recommendation-list">
        {recommendations.map((rec, idx) => (
          <div key={idx} className="recommendation-item">
            <div className="rec-rank">{idx + 1}</div>
            <div className="rec-info">
              <div className="rec-name">{rec.franchise.name}</div>
              <div className="rec-details">
                Setup: {formatCurrency(rec.franchise.setup_cost)} •
                Margin: {rec.franchise.profit_margin}% •
                Employees: {rec.franchise.employees_required}
              </div>
              {rec.reasons && rec.reasons.length > 0 && (
                <ul className="rec-reasons">
                  {rec.reasons.map((reason, ridx) => (
                    <li key={ridx}>{reason}</li>
                  ))}
                </ul>
              )}
            </div>
            <span className="rec-score">{rec.score}</span>
          </div>
        ))}
    </div>
  );
}

export default RecommendationPanel;
