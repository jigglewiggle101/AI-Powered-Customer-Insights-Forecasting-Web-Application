// frontend/src/components/churnpanel.tsx
import React from 'react';

type Item = { customer_id: string; recency: number; frequency: number; monetary: number; churn_probability: number };

export default function ChurnPanel({ items, onTrain }: { items: Item[]; onTrain: () => void }) {
  return (
    <div className="card">
      <div className="flex" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
        <h3>Churn risk (top 50)</h3>
        <button onClick={onTrain}>Train churn model</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Customer</th><th>Recency</th><th>Frequency</th><th>Monetary</th><th>Risk</th>
          </tr>
        </thead>
        <tbody>
          {items.map((r) => (
            <tr key={r.customer_id}>
              <td>{r.customer_id}</td>
              <td>{r.recency}</td>
              <td>{r.frequency}</td>
              <td>${r.monetary.toFixed(2)}</td>
              <td>{(r.churn_probability * 100).toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}