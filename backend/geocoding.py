"""
Geocoding Service - Converts area names to latitude/longitude coordinates.
Uses OpenStreetMap Nominatim (free, no API key required).
"""
import time
import json
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from config import Config

GEOCACHE_PATH = os.path.join(Config.DATA_DIR, 'geocache.json')

# Pre-built coordinates for Indian states/UTs (fallback)
STATE_COORDINATES = {
    "Jammu & Kashmir": (33.7782, 76.5762),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Punjab": (31.1471, 75.3412),
    "Chandigarh": (30.7333, 76.7794),
    "Uttarakhand": (30.0668, 79.0193),
    "Haryana": (29.0588, 76.0856),
    "Nct Of Delhi": (28.7041, 77.1025),
    "Rajasthan": (27.0238, 74.2179),
    "Uttar Pradesh": (26.8467, 80.9462),
    "Bihar": (25.0961, 85.3131),
    "Sikkim": (27.5330, 88.5122),
    "Arunachal Pradesh": (28.2180, 94.7278),
    "Nagaland": (26.1584, 94.5624),
    "Manipur": (24.6637, 93.9063),
    "Mizoram": (23.1645, 92.9376),
    "Tripura": (23.9408, 91.9882),
    "Meghalaya": (25.4670, 91.3662),
    "Assam": (26.2006, 92.9376),
    "West Bengal": (22.9868, 87.8550),
    "Jharkhand": (23.6102, 85.2799),
    "Odisha": (20.9517, 85.0985),
    "Chhattisgarh": (21.2787, 81.8661),
    "Madhya Pradesh": (22.9734, 78.6569),
    "Gujarat": (22.2587, 71.1924),
    "Daman & Diu": (20.4283, 72.8397),
    "Dadra & Nagar Haveli": (20.1809, 73.0169),
    "Maharashtra": (19.7515, 75.7139),
    "Andhra Pradesh": (15.9129, 79.7400),
    "Karnataka": (15.3173, 75.7139),
    "Goa": (15.2993, 74.1240),
    "Lakshadweep": (10.5667, 72.6417),
    "Kerala": (10.8505, 76.2711),
    "Tamil Nadu": (11.1271, 78.6569),
    "Puducherry": (11.9416, 79.8083),
    "Andaman & Nicobar Islands": (11.7401, 92.6586),
    "Telangana": (18.1124, 79.0193),
}


def load_geocache():
    """Load cached geocoding results."""
    if os.path.exists(GEOCACHE_PATH):
        with open(GEOCACHE_PATH, 'r') as f:
            return json.load(f)
    return {}


def save_geocache(cache):
    """Save geocoding results to cache."""
    os.makedirs(os.path.dirname(GEOCACHE_PATH), exist_ok=True)
    with open(GEOCACHE_PATH, 'w') as f:
        json.dump(cache, f, indent=2)


def geocode_area(area_name, country="India"):
    """Convert area name to coordinates using Nominatim with caching."""
    cache = load_geocache()

    if area_name in cache:
        return cache[area_name]

    # Check pre-built coordinates first
    if area_name in STATE_COORDINATES:
        lat, lon = STATE_COORDINATES[area_name]
        cache[area_name] = {"latitude": lat, "longitude": lon}
        save_geocache(cache)
        return cache[area_name]

    # Try Nominatim geocoding
    geolocator = Nominatim(user_agent="franchise_dna_app")
    try:
        location = geolocator.geocode(f"{area_name}, {country}", timeout=10)
        if location:
            result = {"latitude": location.latitude, "longitude": location.longitude}
            cache[area_name] = result
            save_geocache(cache)
            time.sleep(1)  # Respect rate limits
            return result
    except (GeocoderTimedOut, GeocoderServiceError):
        pass

    return None


def geocode_all_areas(area_names):
    """Geocode a list of area names and return results."""
    results = {}
    for area in area_names:
        coords = geocode_area(area)
        if coords:
            results[area] = coords
        else:
            print(f"Warning: Could not geocode '{area}'")
    return results


if __name__ == '__main__':
    # Test geocoding
    test_areas = ["Tamil Nadu", "Maharashtra", "Karnataka"]
    results = geocode_all_areas(test_areas)
    for area, coords in results.items():
        print(f"{area}: {coords}")
