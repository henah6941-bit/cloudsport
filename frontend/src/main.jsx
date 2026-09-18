import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import './style.css';

function App() {
  const [data, setData] = useState(null); const [error, setError] = useState('');
  useEffect(() => { fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/fixtures`).then(r => r.json()).then(setData).catch(e => setError(e.message)); }, []);
  return <main><h1>CloudSport</h1><p>Football predictions</p>{error && <p className="error">{error}</p>}{data?.warning && <p className="warning">{data.warning}</p>}<section>{data?.fixtures?.map(f => <article key={f.id}><h2>{f.home_team} — {f.away_team}</h2><small>{f.league || 'Football'} · {new Date(f.kickoff_at).toLocaleString()}</small>{f.predictions.map(p => <div className="prediction" key={p.market}><b>{p.market}: {p.selection}</b><span>{Math.round(p.confidence * 100)}%</span><p>{p.explanation}</p></div>)}</article>)}</section>{data && !data.fixtures.length && <p>No fixtures available.</p>}</main>;
}
createRoot(document.getElementById('root')).render(<App />);
