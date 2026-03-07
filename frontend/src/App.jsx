import React, { useState, useEffect, useCallback } from 'react';
import MapView from './components/MapView';
import Dashboard from './components/Dashboard';
import LandingPage from './components/LandingPage';
import FranchiseSelector from './components/FranchiseSelector';
import RadiusSelector from './components/RadiusSelector';
import Logo from './components/Logo';
import PopulationStats from './components/PopulationStats';
import CompetitorPanel from './components/CompetitorPanel';
import ProfitPrediction from './components/ProfitPrediction';
import RiskAnalysis from './components/RiskAnalysis';
import RecommendationPanel from './components/RecommendationPanel';
import { runAnalysis, getFranchises, getPopulationData, generatePdfReport, geocodeArea } from './services/api';

function App() {
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [locationName, setLocationName] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [radius, setRadius] = useState(3);
  const [selectedFranchise, setSelectedFranchise] = useState(null);
  const [franchises, setFranchises] = useState([]);
  const [populationAreas, setPopulationAreas] = useState([]);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('landing');

  useEffect(() => {
    getFranchises()
      .then(res => {
        setFranchises(res.data.franchises);
        if (res.data.franchises.length > 0) {
          setSelectedFranchise(res.data.franchises[0]);
        }
      })
      .catch(() => setError('Failed to load franchise types'));

    getPopulationData()
      .then(res => setPopulationAreas(res.data.areas))
      .catch(() => {});
  }, []);

  const handleMapClick = useCallback((latlng) => {
    setSelectedLocation(latlng);
    setLocationName(`${latlng.lat.toFixed(4)}, ${latlng.lng.toFixed(4)}`);
    setAnalysisResult(null);
  }, []);

  const handleLocationSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearching(true);
    setError(null);
    try {
      const res = await geocodeArea(searchQuery.trim());
      if (res.data && res.data.latitude && res.data.longitude) {
        const latlng = { lat: res.data.latitude, lng: res.data.longitude };
        setSelectedLocation(latlng);
        setLocationName(searchQuery.trim());
        setAnalysisResult(null);
      } else {
        setError('Location not found. Try a different name.');
      }
    } catch {
      setError('Could not find that location. Try a city or village name in India.');
    } finally {
      setSearching(false);
    }
  };

  const handleSearchKeyDown = (e) => {
    if (e.key === 'Enter') handleLocationSearch();
  };

  const handleAnalyze = async () => {
    if (!selectedLocation) {
      setError('Please select a location on the map');
      return;
    }
    if (!selectedFranchise) {
      setError('Please select a franchise type');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await runAnalysis({
        latitude: selectedLocation.lat,
        longitude: selectedLocation.lng,
        radius_km: radius,
        franchise_id: selectedFranchise.id,
        location_name: locationName,
      });
      setAnalysisResult(response.data);
      setActiveTab('dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!analysisResult) return;
    try {
      const response = await generatePdfReport(analysisResult);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'FranchiseDNA_Report.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      setError('Failed to generate PDF report');
    }
  };

  if (activeTab === 'landing') {
    return <LandingPage onEnter={() => setActiveTab('map')} />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo" onClick={() => setActiveTab('landing')}>
            <Logo size={28} light />
            <h1>FranchiseDNA</h1>
          </div>
          <p className="tagline">Location Intelligence</p>
        </div>
        <nav className="header-nav">
          <button
            className={`nav-btn ${activeTab === 'map' ? 'active' : ''}`}
            onClick={() => setActiveTab('map')}
          >
            Map
          </button>
          <button
            className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
            disabled={!analysisResult}
          >
            Dashboard
          </button>
          {analysisResult && (
            <button className="nav-btn pdf-btn" onClick={handleDownloadPdf}>
              PDF
            </button>
          )}
        </nav>
      </header>

      {error && (
        <div className="error-banner">
          <span>{error}</span>
          <button onClick={() => setError(null)}>&#x2715;</button>
        </div>
      )}

      <main className="app-main">
        {activeTab === 'map' && (
          <div className="map-layout">
            <aside className="sidebar">
              <div className="sidebar-section">
                <h3>Search Location</h3>
                <div className="location-search-group">
                  <input
                    type="text"
                    className="location-input"
                    placeholder="Enter city, village or area..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyDown={handleSearchKeyDown}
                  />
                  <button
                    className="search-btn"
                    onClick={handleLocationSearch}
                    disabled={searching || !searchQuery.trim()}
                  >
                    {searching ? (
                      <span className="spinner"></span>
                    ) : (
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
                      </svg>
                    )}
                  </button>
                </div>
                {selectedLocation && (
                  <p className="coords-display">
                    {locationName} ({selectedLocation.lat.toFixed(4)}, {selectedLocation.lng.toFixed(4)})
                  </p>
                )}
              </div>

              <RadiusSelector radius={radius} onChange={setRadius} />

              <FranchiseSelector
                franchises={franchises}
                selected={selectedFranchise}
                onChange={setSelectedFranchise}
              />

              <button
                className={`analyze-btn ${loading ? 'loading' : ''}`}
                onClick={handleAnalyze}
                disabled={loading || !selectedLocation}
              >
                {loading ? (
                  <><span className="spinner"></span> Analyzing...</>
                ) : (
                  'Analyze Location'
                )}
              </button>

              {analysisResult && (
                <div className="quick-stats">
                  <h3>Quick Results</h3>
                  <div className="stat-item">
                    <span>Population</span>
                    <strong>{analysisResult.population.total_population.toLocaleString()}</strong>
                  </div>
                  <div className="stat-item">
                    <span>Competitors</span>
                    <strong>{analysisResult.competitors.total_count}</strong>
                  </div>
                  <div className="stat-item">
                    <span>Daily Revenue</span>
                    <strong>₹{Math.round(analysisResult.profit.daily_revenue).toLocaleString()}</strong>
                  </div>
                  <div className={`stat-item risk-${analysisResult.risk.risk_level.toLowerCase()}`}>
                    <span>Risk Level</span>
                    <strong>{analysisResult.risk.risk_level}</strong>
                  </div>
                </div>
              )}
            </aside>

            <div className="map-container">
              <MapView
                selectedLocation={selectedLocation}
                radius={radius}
                populationAreas={populationAreas}
                competitors={analysisResult?.competitors?.competitors || []}
                onMapClick={handleMapClick}
              />
            </div>
          </div>
        )}

        {activeTab === 'dashboard' && analysisResult && (
          <Dashboard
            data={analysisResult}
            onBack={() => setActiveTab('map')}
            onDownloadPdf={handleDownloadPdf}
          />
        )}
      </main>
    </div>
  );
}

export default App;
