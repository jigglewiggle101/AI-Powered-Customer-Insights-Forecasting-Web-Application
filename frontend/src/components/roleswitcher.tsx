// frontend/src/components/RoleSwitcher.tsx
import React, { useEffect, useState } from 'react';
import { setApiKey } from '../api';

const ROLES = [
  { label: 'Admin', key: 'demo-key' },
  { label: 'Analyst', key: 'analyst-key' },
  { label: 'Viewer', key: 'viewer-key' },
];

export default function RoleSwitcher({ onChanged }: { onChanged: () => void }) {
  const [key, setKey] = useState(localStorage.getItem('apiKey') || ROLES[0].key);

  useEffect(() => {
    setApiKey(key);   // updates axios header + localStorage
    onChanged();      // reload data when role changes
  }, [key]);

  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <span>Role:</span>
      <select value={key} onChange={(e) => setKey(e.target.value)}>
        {ROLES.map((r) => (
          <option key={r.key} value={r.key}>{r.label}</option>
        ))}
      </select>
    </div>
  );
}