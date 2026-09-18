import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  useEffect(() => {
    fetch(`${API_URL}/api/fixtures`).then(async response => {
      if (!response.ok) throw new Error(`API request failed (${response.status})`);
      return response.json();
    }).then(setData).catch(error => setError(error.message));
  }, []);
  return <main><header><h1>CloudSport</h1><p>Football predictions powered by transparent rules</p></header>
    {error && <p className="error" role="alert">{error}</p>}
    {data?.warning && <p className="warning" role="status">{data.warning}</p>}
    {data && <p className="source">Data source: <strong>{data.source}</strong></p>}
    <section aria-live="polite">{data?.fixtures?.map(f => <article key={f.id}>
      <h2>{f.home_team} <span aria-hidden="true">—</span> {f.away_team}</h2>
      <small>{f.league || 'Football'} · {new Date(f.kickoff_at).toLocaleString()}</small>
      {f.predictions.map(p => <div className="prediction" key={p.market}><b>{p.market.replaceAll('_', ' ')}: {p.selection}</b><span>{Math.round(p.confidence * 100)}%</span><p>{p.explanation}</p></div>)}
    </article>)}</section>
    {data && !data.fixtures.length && <p>No fixtures available.</p>}
  </main>;
}
createRoot(document.getElementById('root')).render(<App />);
