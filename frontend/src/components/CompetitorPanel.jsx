import React, { useState, useMemo } from 'react';

const typeIcons = {
  restaurant: '🍽️',
  cafe: '☕',
  fast_food: '🍔',
  gym: '🏋️',
  pharmacy: '💊',
  shop: '🛒',
  bakery: '🧁',
  clothing: '👗',
  supermarket: '🏪',
  clinic: '🏥',
  salon: '💇',
  jewelry: '💎',
  electronics: '📱',
  education: '🎓',
};

function CompetitorPanel({ data, location }) {
  const [filter, setFilter] = useState('all');
  const [showAll, setShowAll] = useState(false);

  if (!data) return null;

  const competitors = data.competitors || [];

  // Build type breakdown
  const typeCounts = useMemo(() => {
    const counts = {};
    competitors.forEach(c => {
      const t = c.type || 'other';
      counts[t] = (counts[t] || 0) + 1;
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  }, [competitors]);

  const filtered = filter === 'all' ? competitors : competitors.filter(c => c.type === filter);
  const displayed = showAll ? filtered : filtered.slice(0, 15);

  return (
    <>
      {/* Summary row */}
      <div className="competitor-summary">
        <div className="competitor-count-badge">
          <span className="comp-count">{data.total_count}</span> competitors within {data.search_radius_km} km
        </div>
        {data.direct_competitors != null && (
          <div className="competitor-direct-badge">
            {data.direct_competitors} direct
          </div>
        )}
      </div>

      {/* Type filter chips */}
      {typeCounts.length > 1 && (
        <div className="competitor-filters">
          <button
            className={`comp-chip ${filter === 'all' ? 'active' : ''}`}
            onClick={() => { setFilter('all'); setShowAll(false); }}
          >
            All ({competitors.length})
          </button>
          {typeCounts.map(([type, count]) => (
            <button
              key={type}
              className={`comp-chip ${filter === type ? 'active' : ''}`}
              onClick={() => { setFilter(type); setShowAll(false); }}
            >
              {typeIcons[type] || '📍'} {type} ({count})
            </button>
          ))}
        </div>
      )}

      {/* Competitor list */}
      <div className="competitor-list">
        {displayed.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: 13, textAlign: 'center', padding: 20 }}>
            No competitors found in this area
          </p>
        ) : (
          displayed.map((comp, idx) => (
            <div key={idx} className="competitor-item">
              <div className="competitor-icon">
                {typeIcons[comp.type] || '📍'}
              </div>
              <div className="competitor-info">
                <div className="competitor-name">{comp.name}</div>
                <div className="competitor-meta">
                  <span className="competitor-type-label">{comp.type}</span>
                  {comp.brand && <span className="competitor-brand">{comp.brand}</span>}
                  {comp.cuisine && <span className="competitor-cuisine">{comp.cuisine}</span>}
                </div>
                {comp.address && (
                  <div className="competitor-address">{comp.address}</div>
                )}
              </div>
              <div className="competitor-right">
                {comp.rating != null && (
                  <div className="competitor-rating">
                    <span className="star">★</span> {comp.rating}
                    {comp.user_ratings_total > 0 && (
                      <span className="rating-count">({comp.user_ratings_total})</span>
                    )}
                  </div>
                )}
                {comp.distance_km != null && (
                  <div className="competitor-distance">{comp.distance_km} km</div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Show more / less */}
      {filtered.length > 15 && (
        <button className="comp-show-more" onClick={() => setShowAll(!showAll)}>
          {showAll ? 'Show less' : `Show all ${filtered.length} competitors`}
        </button>
      )}
    </>
  );
}

export default CompetitorPanel;
