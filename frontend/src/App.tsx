// frontend/src/App.tsx
import React, { useEffect, useState, useCallback } from 'react';
import {
  getInsights,
  getSegments,
  getForecast,
  seedDemo,
  trainChurn,
  predictChurn,
  getAnomalies,
  getSummaryReport,
} from './api';

import UploadCSV from './components/uploadcsv';
import InsightsCards from './components/insightscards';
import ForecastChart from './components/forecast';
import SegmentTable from './components/segmenttable';
import FiltersBar from './components/filtersbar';
import RoleSwitcher from './components/roleswitcher';
import ChurnPanel from './components/churnpanel';
import Anomalies from './components/anomalies';
import SummaryCard from './components/summarycard';
import useCurrentUser from './hooks/useCurrentUser';

type KPI = { totalRevenue: number; avgOrderValue: number; customers: number; orders: number };
type InsightRes = { kpis: KPI; byCategory: { product_category: string; amount: number }[]; byChannel: { channel: string; amount: number }[] };
type SegmentItem = { customer_id: string; recency: number; frequency: number; monetary: number; segment: string };
type ForecastPoint = { ds: string; yhat: number };
type ChurnItem = { customer_id: string; recency: number; frequency: number; monetary: number; churn_probability: number };
type AnomalyItem = { date: string; amount: number; z: number; is_anomaly: boolean };

export default function App() {
  const [roleKey, setRoleKey] = useState(localStorage.getItem('apiKey')); // track current role key
  const user = useCurrentUser(roleKey);

  const [insights, setInsights] = useState<InsightRes | null>(null);
  const [segments, setSegments] = useState<SegmentItem[]>([]);
  const [forecast, setForecast] = useState<ForecastPoint[]>([]);
  const [churn, setChurn] = useState<ChurnItem[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalyItem[]>([]);
  const [summary, setSummary] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [days, setDays] = useState(30);

  const loadAll = useCallback(async () => {
    setLoading(true);
    try {
      const [i, s, f, c, a, r] = await Promise.all([
        getInsights(),
        getSegments(),
        getForecast(days),
        predictChurn().catch(() => []),
        getAnomalies().catch(() => []),
        getSummaryReport().catch(() => ''),
      ]);
      setInsights(i);
      setSegments(s.segments || []);
      setForecast(f.forecast || []);
      setChurn(c);
      setAnomalies(a);
      setSummary(r);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [days]);

  useEffect(() => { loadAll(); }, []);
  useEffect(() => {
    (async () => {
      const f = await getForecast(days);
      setForecast(f.forecast || []);
    })();
  }, [days]);

  if (!user) return <p>Loading user info...</p>;

  return (
    <div className="container">
      <div className="flex" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>AI Customer Insights</h1>
        <div className="flex" style={{ gap: 12, alignItems: 'center' }}>
          <p>Welcome {user.username} ({user.role})</p>
          <RoleSwitcher onChanged={() => {
            setRoleKey(localStorage.getItem('apiKey')); // refresh user info
            loadAll(); // reload data
          }} />
          {user.role === 'admin' && (
            <>
              <button onClick={async () => { await seedDemo(); await loadAll(); }}>Seed demo data</button>
              <UploadCSV onUploaded={loadAll} />
            </>
          )}
        </div>
      </div>

      <FiltersBar days={days} setDays={setDays} loading={loading} />

      {(user.role === 'admin' || user.role === 'analyst') && summary && (
        <div className="row" style={{ marginTop: 16 }}>
          <div className="col-12">
            <SummaryCard text={summary} />
          </div>
        </div>
      )}

      {(user.role === 'admin' || user.role === 'analyst') && insights && (
        <div className="row" style={{ marginTop: 16 }}>
          <div className="col-12">
            <InsightsCards
              kpis={insights.kpis}
              byCategory={insights.byCategory}
              byChannel={insights.byChannel}
            />
          </div>
        </div>
      )}

      <div className="row" style={{ marginTop: 16 }}>
        <div className="col-6">
          <div className="card">
            <h3>Revenue forecast</h3>
            <ForecastChart forecast={forecast} />
          </div>
        </div>
        <div className="col-6">
          <div className="card">
            <h3>Customer segments (RFM)</h3>
            {(user.role === 'admin' || user.role === 'analyst') && (
              <SegmentTable segments={segments} />
            )}
          </div>
        </div>
      </div>

      {(user.role === 'admin' || user.role === 'analyst') && (
        <div className="row" style={{ marginTop: 16 }}>
          <div className="col-6">
            <ChurnPanel items={churn} onTrain={async () => { await trainChurn(); await loadAll(); }} />
          </div>
          <div className="col-6">
            <Anomalies rows={anomalies} />
          </div>
        </div>
      )}
    </div>
  );
}