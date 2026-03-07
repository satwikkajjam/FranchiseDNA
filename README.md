# FranchiseDNA

A full-stack franchise location analysis platform that helps entrepreneurs evaluate the viability of opening a franchise at any location in India. Analyzes population demographics, competitor landscape, profit potential, and risk — then compares returns against bank fixed deposits.

## Features

- **Interactive Map** — Click any location or search by city/village name to analyze
- **89 Franchise Types** — Indian market store types with real financial data (clothing, food, electronics, services, etc.)
- **Population Analysis** — Demographics, working population, literacy rates from census data
- **Competitor Detection** — Finds nearby competitors via Google Places API and OpenStreetMap
- **Profit Prediction** — Revenue estimation adjusted for population density and competition
- **Bank FD Comparison** — Side-by-side franchise profit vs 7.5% bank fixed deposit returns
- **5-Year Projections** — Revenue growth with inflation-adjusted costs and compound interest comparison
- **Risk Analysis** — Scored risk assessment with actionable factors
- **Franchise Recommendations** — Top 5 franchise suggestions based on area demographics
- **PDF Reports** — Professional downloadable reports with cover page, TOC, and all analysis sections

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask, SQLAlchemy, SQLite |
| Frontend | React 18, Vite 5 |
| Map | Leaflet, react-leaflet |
| Charts | Recharts |
| APIs | Google Places, OpenStreetMap Overpass, Nominatim |
| PDF | ReportLab |
| Geocoding | geopy (Nominatim) |

## Project Structure

```
FranchiseDNA/
├── backend/
│   ├── app.py                  # Flask app with 11 API endpoints
│   ├── population_analysis.py  # Census data processing
│   ├── competitor_detection.py # Google Places + OSM competitor search
│   ├── profit_engine.py        # Revenue prediction + bank FD comparison
│   ├── risk_analysis.py        # Risk scoring engine
│   ├── franchise_data.py       # 89 franchise types seed data
│   ├── geocoding.py            # Nominatim geocoding with caching
│   ├── report_generator.py     # PDF report generation
│   ├── models.py               # SQLAlchemy models
│   └── config.py               # API keys and configuration
├── frontend/
│   └── src/
│       ├── App.jsx             # Main app with search + map
│       ├── App.css             # Dark theme styles
│       ├── components/
│       │   ├── Dashboard.jsx
│       │   ├── MapView.jsx
│       │   ├── ProfitPrediction.jsx
│       │   ├── CompetitorPanel.jsx
│       │   ├── PopulationStats.jsx
│       │   ├── RiskAnalysis.jsx
│       │   ├── RecommendationPanel.jsx
│       │   ├── FranchiseSelector.jsx
│       │   └── LandingPage.jsx
│       └── services/api.js
└── data/
    └── cleaned_population.csv  # Indian census population data
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/population` | Population data by coordinates |
| GET | `/api/population/search` | Search population by area name |
| GET | `/api/franchises` | List all 89 franchise types |
| GET | `/api/franchises/:id` | Get franchise details |
| GET | `/api/geocode` | Geocode area name to coordinates |
| POST | `/api/analyze` | Run full location analysis |
| POST | `/api/report/pdf` | Generate PDF report |
| GET | `/api/reports` | List saved reports |
| GET | `/api/reports/:id` | Get a specific report |
| GET | `/api/heatmap` | Population heatmap data |

## Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Google Places API key

### Backend

```bash
cd backend
python -m venv ../.venv
source ../.venv/bin/activate
pip install -r requirements.txt
python app.py
```

The backend runs on `http://localhost:5002`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:3000` and proxies API calls to the backend.

### Configuration

Add your Google Places API key in `backend/config.py`:

```python
GOOGLE_PLACES_API_KEY = "your-api-key-here"
```

## Usage

1. Start the backend and frontend servers
2. Open `http://localhost:3000`
3. Click on the map or search for a city/village name
4. Select a franchise type and analysis radius
5. Click **Analyze** to get full location analysis
6. Download the PDF report for offline review
