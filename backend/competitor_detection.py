"""
Competitor Detection Module - Finds businesses near a given location.
Uses Google Places API (primary), OpenStreetMap Overpass API (fallback),
or simulated data if both are unavailable.
"""
import requests
import math
from config import Config


# Google Places type mapping
GOOGLE_TYPE_MAP = {
    "restaurant": "restaurant",
    "cafe": "cafe",
    "fast_food": "meal_takeaway",
    "gym": "gym",
    "pharmacy": "pharmacy",
    "clinic": "doctor",
    "shop": "store",
    "supermarket": "supermarket",
    "bakery": "bakery",
    "clothing": "clothing_store",
    "jewelry": "jewelry_store",
    "electronics": "electronics_store",
    "salon": "hair_care",
    "education": "school",
}


def search_competitors_google(latitude, longitude, radius_m, business_type="restaurant"):
    """Search for competitors using Google Places Nearby Search API."""
    api_key = Config.GOOGLE_PLACES_API_KEY
    if not api_key:
        return None  # Signal to fall back

    place_type = GOOGLE_TYPE_MAP.get(business_type, "store")
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": min(radius_m, 50000),
        "type": place_type,
        "key": api_key,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") not in ("OK", "ZERO_RESULTS"):
            return None  # API error, fall back

        competitors = []
        for place in data.get("results", []):
            loc = place.get("geometry", {}).get("location", {})
            competitors.append({
                "name": place.get("name", "Unnamed Business"),
                "type": business_type,
                "latitude": loc.get("lat"),
                "longitude": loc.get("lng"),
                "address": place.get("vicinity", ""),
                "rating": place.get("rating"),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "brand": "",
                "cuisine": "",
            })

        return {
            "competitors": competitors,
            "total_count": len(competitors),
            "source": "Google Places",
            "search_radius_m": radius_m,
            "business_type": business_type,
        }

    except (requests.RequestException, ValueError, KeyError):
        return None  # Fall back


def search_competitors_osm(latitude, longitude, radius_m, business_type="restaurant"):
    """
    Search for competitors using OpenStreetMap Overpass API.
    business_type: restaurant, cafe, fast_food, shop, gym, pharmacy, etc.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"

    # Map business types to OSM tags
    tag_map = {
        "restaurant": '["amenity"="restaurant"]',
        "cafe": '["amenity"="cafe"]',
        "coffee_shop": '["amenity"="cafe"]',
        "fast_food": '["amenity"="fast_food"]',
        "gym": '["leisure"="fitness_centre"]',
        "pharmacy": '["amenity"="pharmacy"]',
        "clinic": '["amenity"="clinic"]',
        "shop": '["shop"]',
        "supermarket": '["shop"="supermarket"]',
        "bakery": '["shop"="bakery"]',
        "clothing": '["shop"="clothes"]',
        "jewelry": '["shop"="jewelry"]',
        "electronics": '["shop"="electronics"]',
        "salon": '["shop"="hairdresser"]',
        "education": '["amenity"="school"]',
    }

    tag = tag_map.get(business_type, '["amenity"="restaurant"]')

    query = f"""
    [out:json][timeout:25];
    (
      node{tag}(around:{radius_m},{latitude},{longitude});
      way{tag}(around:{radius_m},{latitude},{longitude});
    );
    out center body;
    """

    try:
        response = requests.post(overpass_url, data={'data': query}, timeout=10)
        response.raise_for_status()
        data = response.json()

        competitors = []
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            lat = element.get('lat') or element.get('center', {}).get('lat')
            lon = element.get('lon') or element.get('center', {}).get('lon')

            competitors.append({
                'name': tags.get('name', 'Unnamed Business'),
                'type': tags.get('amenity') or tags.get('shop') or tags.get('leisure', business_type),
                'latitude': lat,
                'longitude': lon,
                'cuisine': tags.get('cuisine', ''),
                'brand': tags.get('brand', ''),
                'address': tags.get('addr:full', tags.get('addr:street', '')),
            })

        return {
            'competitors': competitors,
            'total_count': len(competitors),
            'source': 'OpenStreetMap',
            'search_radius_m': radius_m,
            'business_type': business_type,
        }

    except (requests.RequestException, ValueError):
        return generate_simulated_competitors(latitude, longitude, radius_m, business_type)


def generate_simulated_competitors(latitude, longitude, radius_m, business_type):
    """Generate realistic simulated competitor data when API is unavailable."""
    import random
    random.seed(int(abs(latitude * 1000) + abs(longitude * 1000)))

    # Business type templates
    templates = {
        "restaurant": [
            "Domino's Pizza", "Pizza Hut", "KFC", "McDonald's", "Subway",
            "Biryani House", "Madras Cafe", "Thali Junction", "Saravana Bhavan",
            "Local Diner", "Family Restaurant", "Chinese Corner",
        ],
        "cafe": [
            "Starbucks", "Cafe Coffee Day", "Third Wave Coffee", "Blue Tokai",
            "Chai Point", "Chaayos", "Local Tea Shop", "Filter Coffee House",
        ],
        "fast_food": [
            "McDonald's", "KFC", "Burger King", "Domino's", "Subway",
            "Wow Momo", "Faasos", "Chaat Corner",
        ],
        "gym": [
            "Gold's Gym", "Anytime Fitness", "Cult Fit", "Snap Fitness",
            "Local Gym", "Fitness First",
        ],
        "pharmacy": [
            "Apollo Pharmacy", "MedPlus", "Netmeds Store", "1mg Store",
            "Jan Aushadhi", "Local Medical Shop",
        ],
        "clothing": [
            "Pantaloons", "Max Fashion", "Zudio", "Reliance Trends",
            "V-Mart", "Local Boutique", "Raymond",
        ],
        "jewelry": [
            "Tanishq", "Kalyan Jewellers", "Malabar Gold", "Joyalukkas",
            "PC Jeweller", "Local Jeweller",
        ],
        "electronics": [
            "Croma", "Reliance Digital", "Vijay Sales", "Samsung Store",
            "Apple Store", "Local Electronics",
        ],
        "salon": [
            "Naturals", "Green Trends", "Jawed Habib", "Lakme Salon",
            "YLG Salon", "Local Salon",
        ],
        "bakery": [
            "Monginis", "Bakers Inn", "Karachi Bakery", "Hot Breads",
            "Theobroma", "Local Bakery",
        ],
        "supermarket": [
            "Reliance Fresh", "More Supermarket", "Big Bazaar", "D-Mart",
            "Spencer's", "Local Kirana",
        ],
        "clinic": [
            "Apollo Clinic", "Practo Clinic", "Portea Medical",
            "Manipal Clinic", "Local Clinic", "Diagnostic Center",
        ],
        "education": [
            "BYJU'S Center", "Aakash Institute", "FIITJEE",
            "Kumon Center", "Local Coaching", "Vedantu Center",
        ],
    }

    names = templates.get(business_type, templates["restaurant"])

    # Number of competitors based on radius
    base_count = max(3, int(radius_m / 500))
    count = min(base_count + random.randint(0, 5), len(names))

    competitors = []
    selected = random.sample(names, count)
    for name in selected:
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(100, radius_m)
        dlat = (dist / 111320) * math.cos(angle)
        dlon = (dist / (111320 * math.cos(math.radians(latitude)))) * math.sin(angle)

        competitors.append({
            'name': name,
            'type': business_type,
            'latitude': round(latitude + dlat, 6),
            'longitude': round(longitude + dlon, 6),
            'cuisine': '',
            'brand': name if name[0].isupper() else '',
            'address': '',
            'simulated': True,
        })

    return {
        'competitors': competitors,
        'total_count': len(competitors),
        'source': 'Simulated',
        'search_radius_m': radius_m,
        'business_type': business_type,
    }


def detect_all_competitors(latitude, longitude, radius_km, franchise_category="restaurant"):
    """
    Main function to detect competitors of various types near a location.
    Tries Google Places first, falls back to OSM, then simulated data.
    """
    radius_m = int(radius_km * 1000)

    # Try Google Places API first
    result = search_competitors_google(latitude, longitude, radius_m, franchise_category)

    # Fall back to OSM if Google unavailable
    if result is None:
        result = search_competitors_osm(latitude, longitude, radius_m, franchise_category)

    # Also search for related business types
    related_types = {
        "restaurant": ["fast_food", "cafe"],
        "cafe": ["restaurant", "fast_food"],
        "coffee_shop": ["cafe"],
        "fast_food": ["restaurant"],
        "gym": [],
        "pharmacy": ["clinic"],
        "clinic": ["pharmacy"],
        "clothing": [],
        "jewelry": [],
        "electronics": [],
        "salon": [],
        "bakery": ["cafe"],
        "supermarket": ["shop"],
        "education": [],
        "shop": [],
    }

    all_competitors = result['competitors']
    for related in related_types.get(franchise_category, []):
        extra = search_competitors_osm(latitude, longitude, radius_m, related)
        all_competitors.extend(extra['competitors'])

    # Deduplicate by name + approximate location
    seen = set()
    unique = []
    for c in all_competitors:
        key = (c['name'], round(c.get('latitude', 0) or 0, 4))
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return {
        'competitors': unique,
        'total_count': len(unique),
        'direct_competitors': result['total_count'],
        'search_radius_km': radius_km,
        'category': franchise_category,
    }
