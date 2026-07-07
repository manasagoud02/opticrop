import { useEffect, useMemo, useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

const defaultForm = {
  nitrogen: 90,
  phosphorous: 45,
  potassium: 40,
  temperature: 24,
  humidity: 76,
  ph: 6.2,
  rainfall: 160,
};

function App() {
  const [form, setForm] = useState(defaultForm);
  const [recommendations, setRecommendations] = useState([]);
  const [token, setToken] = useState(localStorage.getItem('opticrop_token') || '');
  const [authMode, setAuthMode] = useState('login');
  const [authData, setAuthData] = useState({ name: '', email: '', password: '' });
  const [message, setMessage] = useState('');
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);

  const isLoggedIn = Boolean(token);

  useEffect(() => {
    if (token) {
      fetchDashboard();
    }
  }, [token]);

  const fetchDashboard = async () => {
    try {
      const res = await axios.get(`${API_BASE}/dashboard`, { headers: { Authorization: `Bearer ${token}` } });
      setDashboard(res.data);
    } catch {
      setMessage('Unable to load dashboard right now.');
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: Number(value) }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setMessage('');
    try {
      const res = await axios.post(`${API_BASE}/recommend`, form, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setRecommendations(res.data.recommendations || []);
      setMessage(`Top crop: ${res.data.top_crop?.crop_name || 'N/A'}`);
      await fetchDashboard();
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Recommendation request failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleAuthSubmit = async (event) => {
    event.preventDefault();
    try {
      const endpoint = authMode === 'login' ? '/auth/login' : '/auth/register';
      const res = await axios.post(`${API_BASE}${endpoint}`, {
        name: authData.name,
        email: authData.email,
        password: authData.password,
      });
      localStorage.setItem('opticrop_token', res.data.token);
      setToken(res.data.token);
      setMessage(authMode === 'login' ? 'Welcome back to OptiCrop.' : 'Account created successfully.');
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Authentication failed.');
    }
  };

  const stats = useMemo(() => {
    if (!recommendations.length) {
      return { topScore: 0, topCrop: 'Waiting for analysis' };
    }
    const top = recommendations[0];
    return { topScore: top.score, topCrop: top.crop_name };
  }, [recommendations]);

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Smart Agricultural Production Optimization Engine</p>
          <h1>OptiCrop helps farmers make better planting decisions.</h1>
          <p className="hero-copy">
            Blend fertilizer, weather, and soil data to identify high-potential crops, assess suitability, and support research planning.
          </p>
        </div>
        <div className="card hero-card">
          <h3>Live insight</h3>
          <p>Top crop score</p>
          <strong>{stats.topScore}%</strong>
          <span>{stats.topCrop}</span>
        </div>
      </header>

      <main className="content-grid">
        <section className="card">
          <h2>Analyze your field</h2>
          <form onSubmit={handleSubmit}>
            {Object.entries(defaultForm).map(([key, value]) => (
              <label key={key}>
                <span>{key}</span>
                <input name={key} type="number" value={form[key]} onChange={handleChange} />
              </label>
            ))}
            <button type="submit" disabled={loading}>{loading ? 'Analyzing...' : 'Recommend Crop'}</button>
          </form>
          {message ? <p className="message">{message}</p> : null}
        </section>

        <section className="card">
          <h2>{isLoggedIn ? 'Your dashboard' : 'Access account'}</h2>
          {!isLoggedIn ? (
            <form onSubmit={handleAuthSubmit}>
              <div className="tabs">
                <button type="button" className={authMode === 'login' ? 'active' : ''} onClick={() => setAuthMode('login')}>Login</button>
                <button type="button" className={authMode === 'register' ? 'active' : ''} onClick={() => setAuthMode('register')}>Register</button>
              </div>
              {authMode === 'register' ? (
                <label>
                  <span>Name</span>
                  <input value={authData.name} onChange={(e) => setAuthData({ ...authData, name: e.target.value })} />
                </label>
              ) : null}
              <label>
                <span>Email</span>
                <input type="email" value={authData.email} onChange={(e) => setAuthData({ ...authData, email: e.target.value })} />
              </label>
              <label>
                <span>Password</span>
                <input type="password" value={authData.password} onChange={(e) => setAuthData({ ...authData, password: e.target.value })} />
              </label>
              <button type="submit">{authMode === 'login' ? 'Login' : 'Create account'}</button>
            </form>
          ) : (
            <>
              <p>Signed in as {dashboard?.user?.name || 'farmer'}.</p>
              <ul>
                {(dashboard?.history || []).map((item, index) => (
                  <li key={`${item.crop_name}-${index}`}>
                    <strong>{item.crop_name}</strong> — {item.score}%
                  </li>
                ))}
              </ul>
            </>
          )}
        </section>
      </main>

      <section className="card results-card">
        <h2>Recommendation results</h2>
        <div className="results-list">
          {recommendations.map((item) => (
            <article key={item.crop_name} className="result-item">
              <div>
                <h3>{item.crop_name}</h3>
                <p>{item.reason}</p>
              </div>
              <div className="result-meta">
                <strong>{item.score}%</strong>
                <span>{item.productivity}</span>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;
