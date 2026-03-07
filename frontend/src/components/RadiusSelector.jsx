import React from 'react';

function RadiusSelector({ radius, onChange }) {
  const options = [1, 3, 5, 10, 15];

  return (
    <div className="radius-selector">
      <h3>Analysis Radius</h3>
      <div className="radius-options">
        {options.map((r) => (
          <button
            key={r}
            className={`radius-btn ${radius === r ? 'active' : ''}`}
            onClick={() => onChange(r)}
          >
            {r} km
          </button>
        ))}
      </div>
    </div>
  );
}

export default RadiusSelector;
