// frontend/src/components/summarycard.tsx
import React from 'react';
export default function SummaryCard({ text }: { text: string }) {
  return (
    <div className="card">
      <h3>Auto summary</h3>
      <p>{text}</p>
    </div>
  );
}