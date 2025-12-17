// frontend/src/components/anomalies.tsx
import React from 'react';
type Row = { date: string; amount: number; z: number; is_anomaly: boolean };

export default function Anomalies({ rows }: { rows: Row[] }) {
  return (
    <div className="card">
      <h3>Revenue anomalies (z-score ≥ threshold)</h3>
      <table>
        <thead>
          <tr><th>Date</th><th>Amount</th><th>Z</th></tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.date} style={{ color: r.is_anomaly ? 'tomato' : undefined }}>
              <td>{r.date}</td>
              <td>${r.amount.toFixed(2)}</td>
              <td>{r.z.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}