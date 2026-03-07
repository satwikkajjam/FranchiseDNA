"""
Population Analysis Module - Calculates population metrics within a given radius.
Uses the Haversine formula for distance calculation.
"""
import math
from models import PopulationData


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points
    on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def analyze_population(latitude, longitude, radius_km):
    """
    Analyze population within a given radius of a location.
    Returns aggregated population statistics.
    """
    all_areas = PopulationData.query.filter(
        PopulationData.latitude.isnot(None),
        PopulationData.longitude.isnot(None)
    ).all()

    nearby_areas = []
    total_population = 0
    total_working = 0
    total_households = 0
    total_literate = 0

    # State approximate areas in sq km for density calculation
    STATE_AREAS = {
        "Jammu & Kashmir": 222236, "Himachal Pradesh": 55673,
        "Punjab": 50362, "Chandigarh": 114, "Uttarakhand": 53483,
        "Haryana": 44212, "Nct Of Delhi": 1484, "Rajasthan": 342239,
        "Uttar Pradesh": 240928, "Bihar": 94163, "Sikkim": 7096,
        "Arunachal Pradesh": 83743, "Nagaland": 16579, "Manipur": 22327,
        "Mizoram": 21081, "Tripura": 10486, "Meghalaya": 22429,
        "Assam": 78438, "West Bengal": 88752, "Jharkhand": 79714,
        "Odisha": 155707, "Chhattisgarh": 135191, "Madhya Pradesh": 308245,
        "Gujarat": 196024, "Daman & Diu": 112, "Dadra & Nagar Haveli": 491,
        "Maharashtra": 307713, "Andhra Pradesh": 275045, "Karnataka": 191791,
        "Goa": 3702, "Lakshadweep": 32, "Kerala": 38863,
        "Tamil Nadu": 130058, "Puducherry": 479,
        "Andaman & Nicobar Islands": 8249, "Telangana": 112077,
    }

    # Find nearest state for density-based estimation
    nearest = min(all_areas, key=lambda a: haversine_distance(
        latitude, longitude, a.latitude, a.longitude
    )) if all_areas else None

    if nearest:
        nearest_distance = haversine_distance(latitude, longitude, nearest.latitude, nearest.longitude)
        state_area = STATE_AREAS.get(nearest.area, 100000)
        state_density = nearest.population / state_area  # people per sq km

        # Urban density multiplier: if within 200km of state capital, assume urban
        # Average Indian urban density: ~3000-10000 per sq km
        if nearest_distance < 50:
            urban_factor = 8.0  # Inside a major city
        elif nearest_distance < 200:
            urban_factor = 4.0  # Near a city
        else:
            urban_factor = 1.5  # Rural/semi-urban

        effective_density = min(state_density * urban_factor, 15000)  # Cap at 15k/sqkm
        effective_density = max(effective_density, 500)  # Floor at 500/sqkm

        analysis_area = math.pi * radius_km ** 2
        total_population = int(effective_density * analysis_area)
        work_ratio = nearest.working_population / nearest.population if nearest.population else 0.4
        lit_ratio = nearest.literacy_rate / 100 if nearest.literacy_rate else 0.7
        total_working = int(total_population * work_ratio)
        total_households = int(total_population / 4.5)
        total_literate = int(total_population * lit_ratio)

        nearby_areas.append({
            'area': nearest.area,
            'distance_km': round(nearest_distance, 2),
            'population': total_population,
            'working_population': total_working,
            'households': total_households,
            'literacy_rate': nearest.literacy_rate,
            'overlap_factor': 1.0,
        })

    # Add other nearby states for context
    for area in all_areas:
        if nearest and area.id == nearest.id:
            continue
        distance = haversine_distance(latitude, longitude, area.latitude, area.longitude)
        if distance <= radius_km * 50:  # Show nearby states for context
            nearby_areas.append({
                'area': area.area,
                'distance_km': round(distance, 2),
                'population': area.population,
                'working_population': area.working_population,
                'households': area.households,
                'literacy_rate': area.literacy_rate,
                'overlap_factor': 0.0,
            })

    avg_literacy = round((total_literate / total_population * 100), 2) if total_population > 0 else 0

    return {
        'latitude': latitude,
        'longitude': longitude,
        'radius_km': radius_km,
        'total_population': total_population,
        'working_population': total_working,
        'total_households': total_households,
        'avg_literacy_rate': avg_literacy,
        'areas_found': len(nearby_areas),
        'nearby_areas': sorted(nearby_areas, key=lambda x: x['distance_km']),
        'population_density': round(total_population / (math.pi * radius_km ** 2), 1) if radius_km > 0 else 0,
    }
