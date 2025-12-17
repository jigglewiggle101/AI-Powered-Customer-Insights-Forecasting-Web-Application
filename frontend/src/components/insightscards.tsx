import React from 'react';

export default function InsightsCards({
  kpis,
  byCategory,
  byChannel
}: {
  kpis?: { totalRevenue: number; avgOrderValue: number; customers: number; orders: number };
  byCategory?: { product_category: string; amount: number }[];
  byChannel?: { channel: string; amount: number }[];
}) {
  // Guard against missing data
  if (!kpis) {
    return (
      <div className="card">
        <h3>No insights yet</h3>
        <p>Seed demo data or upload a CSV to see KPIs.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="row">
        <div className="col-6">
          <div className="card">
            <div className="kpi">
              <div className="kpi-value">${kpis.totalRevenue.toFixed(2)}</div>
              <div className="kpi-label">Total revenue</div>
            </div>
          </div>
        </div>
        <div className="col-6">
          <div className="card">
            <div className="kpi">
              <div className="kpi-value">${kpis.avgOrderValue.toFixed(2)}</div>
              <div className="kpi-label">Average order value</div>
            </div>
          </div>
        </div>
        <div className="col-6">
          <div className="card">
            <div className="kpi">
              <div className="kpi-value">{kpis.customers}</div>
              <div className="kpi-label">Customers</div>
            </div>
          </div>
        </div>
        <div className="col-6">
          <div className="card">
            <div className="kpi">
              <div className="kpi-value">{kpis.orders}</div>
              <div className="kpi-label">Orders</div>
            </div>
          </div>
        </div>
      </div>

      <div className="row" style={{ marginTop: 16 }}>
        <div className="col-6">
          <h3>Revenue by category</h3>
          <table className="table">
            <thead>
              <tr><th>Category</th><th>Revenue</th></tr>
            </thead>
            <tbody>
              {byCategory?.map((c) => (
                <tr key={c.product_category}>
                  <td><span className="badge">{c.product_category}</span></td>
                  <td>${c.amount.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="col-6">
          <h3>Revenue by channel</h3>
          <table className="table">
            <thead>
              <tr><th>Channel</th><th>Revenue</th></tr>
            </thead>
            <tbody>
              {byChannel?.map((c) => (
                <tr key={c.channel}>
                  <td><span className="badge">{c.channel}</span></td>
                  <td>${c.amount.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}