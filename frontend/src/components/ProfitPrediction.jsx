import React from 'react';

function formatCurrency(amount) {
  const abs = Math.abs(amount);
  const sign = amount < 0 ? '-' : '';
  if (abs >= 10000000) return `${sign}₹${(abs / 10000000).toFixed(2)} Cr`;
  if (abs >= 100000) return `${sign}₹${(abs / 100000).toFixed(2)} L`;
  if (abs >= 1000) return `${sign}₹${(abs / 1000).toFixed(1)}K`;
  return `${sign}₹${Math.round(abs).toLocaleString()}`;
}

function ProfitPrediction({ profitData, projections }) {
  if (!profitData) return null;

  const franchiseBetter = profitData.franchise_vs_bank > 0;

  return (
    <>
      {/* Highlight boxes */}
      <div className="profit-highlight">
        <div className="profit-box revenue">
          <span className="amount">{formatCurrency(profitData.yearly_revenue)}</span>
          <span className="label">Yearly Revenue</span>
        </div>
        <div className="profit-box expenses">
          <span className="amount">{formatCurrency(profitData.total_yearly_expenses)}</span>
          <span className="label">Yearly Expenses</span>
        </div>
        <div className="profit-box profit">
          <span className="amount">{formatCurrency(profitData.yearly_profit)}</span>
          <span className="label">Yearly Profit</span>
        </div>
      </div>

      {/* Detail Grid */}
      <div className="profit-details">
        <div className="profit-detail-item">
          <span>Daily Customers</span>
          <strong>{profitData.customers_per_day.toLocaleString()}</strong>
        </div>
        <div className="profit-detail-item">
          <span>Daily Revenue</span>
          <strong>{formatCurrency(profitData.daily_revenue)}</strong>
        </div>
        <div className="profit-detail-item">
          <span>Monthly Revenue</span>
          <strong>{formatCurrency(profitData.monthly_revenue)}</strong>
        </div>
        <div className="profit-detail-item">
          <span>Operating Cost/yr</span>
          <strong>{formatCurrency(profitData.yearly_operating_cost)}</strong>
        </div>
        <div className="profit-detail-item">
          <span>ROI</span>
          <strong>{profitData.roi_percentage.toFixed(1)}%</strong>
        </div>
        <div className="profit-detail-item">
          <span>Break-even</span>
          <strong>{profitData.months_to_breakeven > 0 ? `${profitData.months_to_breakeven} months` : 'N/A'}</strong>
        </div>
        <div className="profit-detail-item">
          <span>Investment</span>
          <strong>{formatCurrency(profitData.total_investment)}</strong>
        </div>
        <div className="profit-detail-item">
          <span>Profit Margin</span>
          <strong>{profitData.actual_profit_margin.toFixed(1)}%</strong>
        </div>
      </div>

      {/* Franchise vs Bank FD Comparison */}
      <h4 style={{ margin: '24px 0 12px', fontSize: 13, fontWeight: 600, color: 'var(--text-secondary)', letterSpacing: '1px', textTransform: 'uppercase' }}>
        Franchise vs Bank FD ({profitData.bank_fd_rate}% p.a.)
      </h4>
      <div className="comparison-table-wrap">
        <table className="projection-table">
          <thead>
            <tr>
              <th></th>
              <th>Franchise</th>
              <th>Bank FD</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Investment</td>
              <td>{formatCurrency(profitData.total_investment)}</td>
              <td>{formatCurrency(profitData.total_investment)}</td>
            </tr>
            <tr>
              <td>Yearly Earning</td>
              <td className="positive">{formatCurrency(profitData.yearly_profit)}</td>
              <td style={{ color: '#f59e0b' }}>{formatCurrency(profitData.bank_yearly_interest)}</td>
            </tr>
            <tr>
              <td>Yearly Return %</td>
              <td className="positive">{profitData.roi_percentage.toFixed(1)}%</td>
              <td style={{ color: '#f59e0b' }}>{profitData.bank_fd_rate}%</td>
            </tr>
            <tr>
              <td>Verdict</td>
              <td colSpan={2} style={{ textAlign: 'center', fontWeight: 600, color: franchiseBetter ? '#22c55e' : '#f59e0b' }}>
                {franchiseBetter
                  ? `Franchise earns ${formatCurrency(profitData.franchise_vs_bank)} more/yr`
                  : `Bank FD earns ${formatCurrency(Math.abs(profitData.franchise_vs_bank))} more/yr`}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* 5-Year Projections with Bank Comparison */}
      {projections && projections.length > 0 && (
        <>
          <h4 style={{ margin: '24px 0 12px', fontSize: 13, fontWeight: 600, color: 'var(--text-secondary)', letterSpacing: '1px', textTransform: 'uppercase' }}>
            5-Year Projections
          </h4>
          <table className="projection-table">
            <thead>
              <tr>
                <th>Year</th>
                <th>Revenue</th>
                <th>Expenses</th>
                <th>Profit</th>
                <th>Cumulative</th>
                <th>Bank Interest</th>
                <th>Bank Cumulative</th>
              </tr>
            </thead>
            <tbody>
              {projections.map((p) => (
                <tr key={p.year}>
                  <td>Year {p.year}</td>
                  <td>{formatCurrency(p.revenue)}</td>
                  <td>{formatCurrency(p.expenses)}</td>
                  <td className={p.profit >= 0 ? 'positive' : 'negative'}>
                    {formatCurrency(p.profit)}
                  </td>
                  <td className={p.cumulative_profit >= 0 ? 'positive' : 'negative'}>
                    {formatCurrency(p.cumulative_profit)}
                  </td>
                  <td style={{ color: '#f59e0b' }}>{formatCurrency(p.bank_interest)}</td>
                  <td style={{ color: '#f59e0b' }}>{formatCurrency(p.cumulative_bank)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </>
  );
}

export default ProfitPrediction;
