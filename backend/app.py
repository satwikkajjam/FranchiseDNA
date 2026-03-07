"""
FranchiseDNA - Main Flask Application
Complete franchise location analysis platform.
"""
import os
import sys
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from config import Config
from models import db, PopulationData, AnalysisReport
from data_processor import get_cleaned_data
from geocoding import geocode_area, geocode_all_areas, STATE_COORDINATES
from population_analysis import analyze_population
from competitor_detection import detect_all_competitors
from franchise_data import (
    seed_franchises, get_all_franchises, get_franchise_by_id,
    recommend_franchises,
)
from profit_engine import predict_profit, generate_projections
from risk_analysis import analyze_risk
from report_generator import generate_report


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        _seed_database()

    return app


def _seed_database():
    """Seed database with cleaned population data and franchise types."""
    # Seed franchise types
    seed_franchises()

    # Seed population data if empty
    if PopulationData.query.count() == 0:
        print("Seeding population data...")
        df = get_cleaned_data()
        for _, row in df.iterrows():
            area_name = row['area']
            coords = STATE_COORDINATES.get(area_name, {})
            lat = coords[0] if isinstance(coords, tuple) else None
            lon = coords[1] if isinstance(coords, tuple) else None

            entry = PopulationData(
                area=area_name,
                latitude=lat,
                longitude=lon,
                population=int(row['population']),
                working_population=int(row['working_population']),
                households=int(row['households']),
                literate_population=int(row.get('literate_population', 0)),
                literacy_rate=float(row.get('literacy_rate', 0)),
            )
            db.session.add(entry)

        db.session.commit()
        print(f"Seeded {PopulationData.query.count()} areas")


app = create_app()


# ==================== API ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'FranchiseDNA API is running'})


# --- Population Data ---
@app.route('/api/population', methods=['GET'])
def get_population_data():
    """Get all population data points for the map."""
    areas = PopulationData.query.all()
    return jsonify({
        'areas': [a.to_dict() for a in areas],
        'total': len(areas),
    })


@app.route('/api/population/search', methods=['GET'])
def search_areas():
    """Search areas by name."""
    query = request.args.get('q', '').strip()
    if not query or len(query) < 2:
        return jsonify({'areas': []})

    areas = PopulationData.query.filter(
        PopulationData.area.ilike(f'%{query}%')
    ).all()
    return jsonify({'areas': [a.to_dict() for a in areas]})


# --- Franchise Types ---
@app.route('/api/franchises', methods=['GET'])
def get_franchises():
    """Get all available franchise types."""
    return jsonify({'franchises': get_all_franchises()})


@app.route('/api/franchises/<int:franchise_id>', methods=['GET'])
def get_franchise(franchise_id):
    """Get a specific franchise type."""
    f = get_franchise_by_id(franchise_id)
    if not f:
        return jsonify({'error': 'Franchise not found'}), 404
    return jsonify(f)


# --- Geocoding ---
@app.route('/api/geocode', methods=['GET'])
def geocode():
    """Geocode an area name to coordinates."""
    area = request.args.get('area', '').strip()
    if not area:
        return jsonify({'error': 'area parameter required'}), 400

    result = geocode_area(area)
    if result:
        return jsonify(result)
    return jsonify({'error': f'Could not geocode: {area}'}), 404


# --- Full Analysis ---
@app.route('/api/analyze', methods=['POST'])
def run_analysis():
    """
    Run complete franchise analysis for a location.
    Expects JSON body:
    {
        "latitude": 12.9815,
        "longitude": 80.2180,
        "radius_km": 3,
        "franchise_id": 1,
        "location_name": "Velachery, Chennai"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    latitude = data.get('latitude')
    longitude = data.get('longitude')
    radius_km = data.get('radius_km', 3)
    franchise_id = data.get('franchise_id')
    location_name = data.get('location_name', f'{latitude}, {longitude}')

    if latitude is None or longitude is None:
        return jsonify({'error': 'latitude and longitude required'}), 400

    # Validate inputs
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        radius_km = float(radius_km)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid numeric values'}), 400

    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        return jsonify({'error': 'Invalid coordinates'}), 400

    if radius_km <= 0 or radius_km > 50:
        return jsonify({'error': 'Radius must be between 0 and 50 km'}), 400

    # 1. Population Analysis
    pop_data = analyze_population(latitude, longitude, radius_km)

    # 2. Get franchise data
    franchise = get_franchise_by_id(franchise_id) if franchise_id else get_all_franchises()[0]
    if not franchise:
        return jsonify({'error': 'Franchise type not found'}), 404

    # 3. Competitor Detection
    comp_data = detect_all_competitors(latitude, longitude, radius_km, franchise.get('category', 'restaurant'))

    # 4. Profit Prediction
    profit_data = predict_profit(pop_data, franchise, comp_data['total_count'])

    # 5. Risk Analysis
    risk_data = analyze_risk(pop_data, franchise, comp_data, profit_data)

    # 6. Franchise Recommendations
    recommendations = recommend_franchises(
        pop_data['total_population'],
        pop_data['working_population'],
        pop_data['avg_literacy_rate'],
        comp_data,
    )

    # 7. Five-Year Projections
    projections = generate_projections(profit_data)

    # Save report to database
    report = AnalysisReport(
        location_name=location_name,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        franchise_id=franchise_id,
        total_population=pop_data['total_population'],
        working_population=pop_data['working_population'],
        total_households=pop_data['total_households'],
        competitor_count=comp_data['total_count'],
        estimated_daily_customers=profit_data['customers_per_day'],
        estimated_daily_revenue=profit_data['daily_revenue'],
        estimated_yearly_revenue=profit_data['yearly_revenue'],
        estimated_yearly_profit=profit_data['yearly_profit'],
        risk_level=risk_data['risk_level'],
        risk_score=risk_data['risk_score'],
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        'report_id': report.id,
        'location': {
            'name': location_name,
            'latitude': latitude,
            'longitude': longitude,
            'radius_km': radius_km,
        },
        'population': pop_data,
        'franchise': franchise,
        'competitors': comp_data,
        'profit': profit_data,
        'risk': risk_data,
        'recommendations': recommendations[:5],
        'projections': projections,
    })


# --- PDF Report ---
@app.route('/api/report/pdf', methods=['POST'])
def generate_pdf_report():
    """Generate and download a PDF report."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Analysis data required'}), 400

    output_path = os.path.join(Config.DATA_DIR, f"report_{data.get('report_id', 'latest')}.pdf")

    try:
        filepath, _ = generate_report(data, output_path)
        return send_file(filepath, as_attachment=True, download_name='FranchiseDNA_Report.pdf')
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500


# --- Analysis History ---
@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get past analysis reports."""
    reports = AnalysisReport.query.order_by(AnalysisReport.created_at.desc()).limit(20).all()
    return jsonify({'reports': [r.to_dict() for r in reports]})


@app.route('/api/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """Get a specific report."""
    report = AnalysisReport.query.get(report_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    return jsonify(report.to_dict())


# --- Heatmap Data ---
@app.route('/api/heatmap', methods=['GET'])
def get_heatmap_data():
    """Get population data formatted for heatmap visualization."""
    areas = PopulationData.query.filter(
        PopulationData.latitude.isnot(None),
        PopulationData.longitude.isnot(None),
    ).all()

    heatmap_points = []
    for a in areas:
        heatmap_points.append({
            'lat': a.latitude,
            'lng': a.longitude,
            'intensity': a.population / 10000000,  # Normalize
            'area': a.area,
            'population': a.population,
        })

    return jsonify({'points': heatmap_points})


if __name__ == '__main__':
    app.run(debug=True, port=5002)
