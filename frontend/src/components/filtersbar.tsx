// frontend/src/components/FiltersBar.tsx
import React from 'react';

export default function filtersbar({
  days, setDays, loading
}: { days: number; setDays: (n: number) => void; loading: boolean }) {
  return (
    <div className="card" style={{ marginTop: 16 }}>
      <div className="flex" style={{ justifyContent: 'space-between' }}>
        <div className="flex">
          <span style={{ color: '#9aa1b2' }}>Forecast horizon:</span>
          <select value={days} onChange={(e) => setDays(Number(e.target.value))} style={{ marginLeft: 8, padding: 6, borderRadius: 8 }}>
            <option value={7}>7 days</option>
            <option value={14}>14 days</option>
            <option value={30}>30 days</option>
            <option value={60}>60 days</option>
          </select>
        </div>
        <div className="badge">{loading ? 'Loading...' : 'Ready'}</div>
      </div>
    </div>
  );
}