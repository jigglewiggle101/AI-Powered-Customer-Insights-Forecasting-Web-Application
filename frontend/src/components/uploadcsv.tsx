import React, { useRef, useState } from 'react';
import { uploadCSV } from '../api';

export default function UploadCSV({ onUploaded }: { onUploaded: () => void }) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [busy, setBusy] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setBusy(true);
    try {
      await uploadCSV(file);   
      onUploaded();
    } finally {
      setBusy(false);
      if (inputRef.current) inputRef.current.value = '';
    }
  };

  return (
    <label style={{ display: 'inline-block' }}>
      <input
        ref={inputRef}
        type="file"
        accept=".csv"
        onChange={handleUpload}
        style={{ display: 'none' }}
      />
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        disabled={busy}
      >
        {busy ? 'Uploading...' : 'Upload CSV'}
      </button>
    </label>
  );
}