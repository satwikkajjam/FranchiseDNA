import React from 'react';

function RiskAnalysis({ data }) {
  if (!data) return null;

  const level = data.risk_level.toLowerCase();

  return (
    <>
      <div className={`risk-overall ${level}`}>
        <span className="risk-level-text">{data.risk_level} Risk</span>
        <span className="risk-score-text">Score: {data.risk_score} / 100</span>
        <div className="risk-meter">
          <div
            className={`risk-meter-fill ${level}`}
            style={{ width: `${data.risk_score}%` }}
          />
        </div>
      </div>

      {/* Risk Factors */}
      <div className="risk-factors">
        {data.risk_factors.map((factor, idx) => (
          <div key={idx} className="risk-factor">
            <span className="risk-factor-name">{factor.factor}</span>
            <div className="risk-factor-bar">
              <div
                className="risk-factor-bar-fill"
                style={{
                  width: `${(factor.score / factor.max_score) * 100}%`,
                  background:
                    factor.level === 'High' ? 'var(--red)' :
                    factor.level === 'Medium' ? 'var(--orange)' : 'var(--green)',
                }}
              />
            </div>
            <span className="risk-factor-score">{factor.score}/{factor.max_score}</span>
            <span className={`risk-factor-level ${factor.level}`}>{factor.level}</span>
          </div>
        ))}
      </div>

      {/* Recommendation */}
      <div className="risk-recommendation">
        <strong>Recommendation:</strong> {data.recommendation}
      </div>
    </>
  );
}

export default RiskAnalysis;
