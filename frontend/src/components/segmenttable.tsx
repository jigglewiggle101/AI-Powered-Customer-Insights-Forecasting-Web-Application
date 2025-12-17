// frontend/src/components/SegmentTable.tsx
import React from 'react';

export default function segmenttable({ segments }: { segments: { customer_id: string; recency: number; frequency: number; monetary: number; segment: string }[] }) {
  return (
    <div>
      <table className="table">
        <thead>
          <tr>
            <th>Customer</th>
            <th>Recency (days)</th>
            <th>Frequency</th>
            <th>Monetary</th>
            <th>Segment</th>
          </tr>
        </thead>
        <tbody>
          {segments.slice(0, 50).map((s) => (
            <tr key={s.customer_id}>
              <td>{s.customer_id}</td>
              <td>{s.recency}</td>
              <td>{s.frequency}</td>
              <td>${s.monetary.toFixed(2)}</td>
              <td><span className="badge">{s.segment}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ color: '#9aa1b2', fontSize: 12, marginTop: 8 }}>Showing first 50 customers</div>
    </div>
  );
}