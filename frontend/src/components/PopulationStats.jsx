import React from 'react';

function PopulationStats({ data }) {
  if (!data) return null;

  return (
    <div className="stats-grid">
        <div className="stat-box">
          <span className="stat-value">{data.total_population.toLocaleString()}</span>
          <span className="stat-label">Total Population</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{data.working_population.toLocaleString()}</span>
          <span className="stat-label">Working Population</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{data.total_households.toLocaleString()}</span>
          <span className="stat-label">Households</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{data.avg_literacy_rate}%</span>
          <span className="stat-label">Literacy Rate</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{data.population_density.toLocaleString()}</span>
          <span className="stat-label">Density / sq km</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{data.areas_found}</span>
          <span className="stat-label">Areas Found</span>
        </div>
    </div>
  );
}

export default PopulationStats;
