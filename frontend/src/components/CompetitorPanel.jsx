import React from 'react';

const typeLabels = {
  restaurant: 'R',
  cafe: 'C',
  fast_food: 'FF',
  gym: 'G',
  pharmacy: 'Ph',
  shop: 'S',
  bakery: 'B',
  clothing: 'Cl',
  supermarket: 'SM',
};

function CompetitorPanel({ data }) {
  if (!data) return null;

  const competitors = data.competitors || [];

  return (
    <>
      <div className="competitor-count-badge">
        {data.total_count} competitors found within {data.search_radius_km} km
      </div>
      <div className="competitor-list">
        {competitors.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: 13, textAlign: 'center', padding: 20 }}>
            No competitors found in this area
          </p>
        ) : (
          competitors.slice(0, 20).map((comp, idx) => (
            <div key={idx} className="competitor-item">
              <div className="competitor-icon">
                {typeLabels[comp.type] || comp.type?.charAt(0)?.toUpperCase() || 'C'}
              </div>
              <div className="competitor-info">
                <div className="competitor-name">{comp.name}</div>
                <div className="competitor-type">
                  {comp.type} {comp.brand ? `• ${comp.brand}` : ''}
                  {comp.cuisine ? ` • ${comp.cuisine}` : ''}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </>
  );
}

export default CompetitorPanel;
