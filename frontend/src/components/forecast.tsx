// frontend/src/components/ForecastChart.tsx
import React from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function forecastchart({ forecast }: { forecast: { ds: string; yhat: number }[] }) {
  const data = forecast.map(f => ({ date: new Date(f.ds).toLocaleDateString(), value: f.yhat }));
  return (
    <div style={{ height: 320 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid stroke="#243046" strokeDasharray="4 4" />
          <XAxis dataKey="date" tick={{ fill: '#9aa1b2' }} />
          <YAxis tick={{ fill: '#9aa1b2' }} />
          <Tooltip contentStyle={{ background: '#121829', border: '1px solid #243046', color: '#e6eaf2' }} />
          <Line type="monotone" dataKey="value" stroke="#6be675" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}