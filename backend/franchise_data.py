"""
Franchise Dataset Module - 90 store types with real Indian market financial data.
"""
from models import db, FranchiseType


# Category mapping for each store type (used for OSM competitor search + grouping)
CATEGORY_MAP = {
    "Clothing Store": "clothing",
    "Gold Shop": "jewelry",
    "Coffee Shop": "cafe",
    "Juice Point": "cafe",
    "Medical Store": "pharmacy",
    "Food Center": "restaurant",
    "Tiffin Center": "restaurant",
    "Vegetable Market": "shop",
    "Bakery": "bakery",
    "Ice Cream Shop": "cafe",
    "Salon": "salon",
    "Gym": "gym",
    "Mobile Store": "electronics",
    "Electronics Store": "electronics",
    "Book Store": "shop",
    "Supermarket": "supermarket",
    "Pet Shop": "shop",
    "Hardware Store": "shop",
    "Stationery Store": "shop",
    "Toy Store": "shop",
    "Fast Food Outlet": "fast_food",
    "Pizza Shop": "fast_food",
    "Tea Shop": "cafe",
    "Sweet Shop": "bakery",
    "Restaurant": "restaurant",
    "Cloud Kitchen": "restaurant",
    "Laundry Shop": "shop",
    "Dry Cleaning": "shop",
    "Flower Shop": "shop",
    "Meat Shop": "shop",
    "Fish Market": "shop",
    "Organic Store": "supermarket",
    "Gift Shop": "shop",
    "Perfume Shop": "shop",
    "Watch Store": "shop",
    "Car Accessories": "shop",
    "Bike Service": "shop",
    "Computer Store": "electronics",
    "Internet Cafe": "cafe",
    "Gaming Cafe": "cafe",
    "Photocopy Shop": "shop",
    "Photography Studio": "shop",
    "Travel Agency": "shop",
    "Courier Service": "shop",
    "Mobile Repair": "electronics",
    "Laptop Repair": "electronics",
    "Car Wash": "shop",
    "Bike Wash": "shop",
    "Water Purifier Store": "shop",
    "Furniture Store": "shop",
    "Mattress Store": "shop",
    "Interior Design Office": "shop",
    "Paint Store": "shop",
    "Tiles Store": "shop",
    "Construction Material Shop": "shop",
    "Pharmacy Franchise": "pharmacy",
    "Dental Clinic": "clinic",
    "Diagnostic Lab": "clinic",
    "Pathology Lab": "clinic",
    "Optical Store": "shop",
    "Footwear Store": "clothing",
    "Sports Shop": "shop",
    "Cycle Store": "shop",
    "Laptop Showroom": "electronics",
    "Camera Store": "electronics",
    "Drone Store": "electronics",
    "Tattoo Studio": "salon",
    "Spa Center": "salon",
    "Yoga Studio": "gym",
    "Dance Studio": "gym",
    "Music Academy": "education",
    "Coaching Center": "education",
    "Play School": "education",
    "Daycare Center": "education",
    "Furniture Repair": "shop",
    "AC Repair Shop": "shop",
    "Electric Repair Shop": "shop",
    "Plumbing Service Shop": "shop",
    "Home Cleaning Service": "shop",
    "Car Rental Office": "shop",
    "Bike Rental Shop": "shop",
    "Event Planning Office": "shop",
    "Wedding Planner Office": "shop",
    "Party Decoration Store": "shop",
    "Balloon Decoration Store": "shop",
    "Printing Press": "shop",
    "Packaging Store": "shop",
    "Plastic Goods Shop": "shop",
    "Kitchen Equipment Store": "shop",
}

# Display categories for frontend grouping
DISPLAY_CATEGORIES = {
    "Food & Beverage": [
        "Coffee Shop", "Juice Point", "Tea Shop", "Food Center", "Tiffin Center",
        "Bakery", "Ice Cream Shop", "Sweet Shop", "Fast Food Outlet", "Pizza Shop",
        "Restaurant", "Cloud Kitchen",
    ],
    "Retail & Shopping": [
        "Clothing Store", "Gold Shop", "Supermarket", "Footwear Store",
        "Organic Store", "Gift Shop", "Perfume Shop", "Watch Store",
        "Toy Store", "Book Store", "Stationery Store", "Sports Shop",
        "Pet Shop", "Flower Shop",
    ],
    "Electronics & Technology": [
        "Mobile Store", "Electronics Store", "Computer Store", "Laptop Showroom",
        "Camera Store", "Drone Store", "Internet Cafe", "Gaming Cafe",
    ],
    "Health & Medical": [
        "Medical Store", "Pharmacy Franchise", "Dental Clinic",
        "Diagnostic Lab", "Pathology Lab", "Optical Store",
    ],
    "Beauty & Wellness": [
        "Salon", "Tattoo Studio", "Spa Center",
    ],
    "Fitness & Sports": [
        "Gym", "Yoga Studio", "Dance Studio", "Cycle Store",
    ],
    "Education & Childcare": [
        "Coaching Center", "Music Academy", "Play School", "Daycare Center",
    ],
    "Food Markets": [
        "Vegetable Market", "Meat Shop", "Fish Market",
    ],
    "Home & Construction": [
        "Furniture Store", "Mattress Store", "Interior Design Office",
        "Paint Store", "Tiles Store", "Construction Material Shop",
        "Hardware Store", "Kitchen Equipment Store", "Water Purifier Store",
    ],
    "Automobile & Transport": [
        "Car Accessories", "Bike Service", "Car Wash", "Bike Wash",
        "Car Rental Office", "Bike Rental Shop",
    ],
    "Repair & Services": [
        "Mobile Repair", "Laptop Repair", "Furniture Repair",
        "AC Repair Shop", "Electric Repair Shop", "Plumbing Service Shop",
        "Laundry Shop", "Dry Cleaning", "Home Cleaning Service",
    ],
    "Events & Media": [
        "Photography Studio", "Event Planning Office", "Wedding Planner Office",
        "Party Decoration Store", "Balloon Decoration Store",
        "Printing Press", "Photocopy Shop",
    ],
    "Logistics & Travel": [
        "Travel Agency", "Courier Service", "Packaging Store",
    ],
    "Others": [
        "Plastic Goods Shop",
    ],
}

# Target demographics by category
TARGET_DEMOGRAPHICS = {
    "cafe": "Youth, Working professionals",
    "restaurant": "Families, Working professionals",
    "fast_food": "Youth, Families",
    "clothing": "Fashion-conscious 18-45",
    "jewelry": "Families, High-income adults",
    "pharmacy": "All demographics",
    "bakery": "Families, Celebrations",
    "salon": "Youth, Working professionals",
    "gym": "Health-conscious 18-45",
    "electronics": "Tech-savvy 18-50",
    "supermarket": "All households",
    "shop": "All demographics",
    "clinic": "All demographics",
    "education": "Students, Parents",
}

# Min population thresholds by category
MIN_POPULATION = {
    "cafe": 10000, "restaurant": 15000, "fast_food": 20000,
    "clothing": 25000, "jewelry": 40000, "pharmacy": 5000,
    "bakery": 10000, "salon": 15000, "gym": 20000,
    "electronics": 20000, "supermarket": 15000, "shop": 8000,
    "clinic": 15000, "education": 15000,
}


def _parse_range_mid(range_str):
    """Parse '800000-1500000' or '10000000+' and return midpoint."""
    range_str = str(range_str).replace(",", "").strip()
    if "+" in range_str:
        return int(range_str.replace("+", ""))
    parts = range_str.split("-")
    if len(parts) == 2:
        return (int(parts[0]) + int(parts[1])) / 2
    return int(parts[0])


def _parse_range(range_str):
    """Parse '800-1200' and return (min, max)."""
    range_str = str(range_str).replace(",", "").strip()
    if "+" in range_str:
        val = int(range_str.replace("+", ""))
        return val, val
    parts = range_str.split("-")
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    return int(parts[0]), int(parts[0])


# Raw data from the user's CSV
_RAW_DATA = [
    ("Clothing Store", "800-1200", "800000-1500000", "1500000-2500000", 20000, 0.25, 5),
    ("Gold Shop", "500-800", "2500000-6000000", "10000000+", 150000, 0.08, 4),
    ("Coffee Shop", "400-800", "600000-1200000", "1200000-2000000", 15000, 0.30, 4),
    ("Juice Point", "150-300", "100000-300000", "300000-500000", 5000, 0.40, 2),
    ("Medical Store", "250-500", "300000-800000", "1000000-1500000", 12000, 0.18, 3),
    ("Food Center", "600-1200", "1000000-2500000", "2000000-4000000", 35000, 0.22, 8),
    ("Tiffin Center", "300-600", "300000-800000", "800000-1500000", 20000, 0.35, 4),
    ("Vegetable Market", "200-400", "50000-200000", "300000-600000", 7000, 0.20, 2),
    ("Bakery", "300-700", "400000-1000000", "1000000-2000000", 12000, 0.30, 4),
    ("Ice Cream Shop", "200-400", "200000-500000", "500000-1000000", 8000, 0.35, 2),
    ("Salon", "300-600", "400000-1000000", "800000-1500000", 10000, 0.40, 4),
    ("Gym", "1500-3000", "2000000-4000000", "3000000-6000000", 20000, 0.30, 5),
    ("Mobile Store", "200-500", "500000-1000000", "1000000-2000000", 20000, 0.15, 3),
    ("Electronics Store", "800-1500", "1000000-2500000", "2500000-4000000", 30000, 0.12, 4),
    ("Book Store", "300-800", "400000-800000", "1000000-1500000", 8000, 0.20, 2),
    ("Supermarket", "1500-3000", "2000000-5000000", "4000000-8000000", 60000, 0.15, 10),
    ("Pet Shop", "300-600", "300000-700000", "800000-1200000", 9000, 0.25, 3),
    ("Hardware Store", "500-1200", "600000-1500000", "2000000-3000000", 25000, 0.18, 4),
    ("Stationery Store", "200-500", "200000-500000", "500000-1000000", 6000, 0.25, 2),
    ("Toy Store", "300-600", "300000-700000", "800000-1500000", 7000, 0.28, 2),
    ("Fast Food Outlet", "400-900", "800000-2000000", "1500000-3000000", 30000, 0.25, 6),
    ("Pizza Shop", "500-900", "1000000-2000000", "2000000-3500000", 35000, 0.28, 6),
    ("Tea Shop", "100-250", "50000-200000", "200000-400000", 4000, 0.40, 2),
    ("Sweet Shop", "400-900", "800000-2000000", "2000000-3000000", 25000, 0.30, 5),
    ("Restaurant", "1200-2500", "2500000-6000000", "5000000-10000000", 60000, 0.20, 12),
    ("Cloud Kitchen", "300-600", "500000-1200000", "1200000-2000000", 20000, 0.30, 4),
    ("Laundry Shop", "200-400", "300000-700000", "800000-1500000", 7000, 0.25, 3),
    ("Dry Cleaning", "300-600", "600000-1200000", "1500000-2000000", 9000, 0.30, 3),
    ("Flower Shop", "100-250", "50000-200000", "200000-500000", 5000, 0.35, 2),
    ("Meat Shop", "200-400", "200000-500000", "600000-1000000", 12000, 0.25, 2),
    ("Fish Market", "200-400", "200000-500000", "600000-1000000", 15000, 0.25, 2),
    ("Organic Store", "300-700", "500000-1200000", "1200000-2000000", 12000, 0.25, 3),
    ("Gift Shop", "200-500", "200000-600000", "500000-1200000", 7000, 0.30, 2),
    ("Perfume Shop", "200-400", "300000-700000", "1000000-1500000", 9000, 0.25, 2),
    ("Watch Store", "200-400", "300000-800000", "1000000-2000000", 12000, 0.18, 2),
    ("Car Accessories", "400-800", "500000-1200000", "1500000-2500000", 20000, 0.20, 3),
    ("Bike Service", "600-1200", "600000-1500000", "1500000-3000000", 25000, 0.25, 4),
    ("Computer Store", "300-700", "500000-1000000", "1500000-2500000", 20000, 0.15, 3),
    ("Internet Cafe", "200-400", "300000-600000", "800000-1200000", 5000, 0.30, 2),
    ("Gaming Cafe", "300-700", "800000-1500000", "1500000-2500000", 12000, 0.35, 3),
    ("Photocopy Shop", "100-250", "100000-300000", "300000-600000", 4000, 0.35, 1),
    ("Photography Studio", "300-600", "400000-1000000", "1000000-2000000", 9000, 0.30, 2),
    ("Travel Agency", "200-400", "200000-500000", "500000-1000000", 7000, 0.25, 2),
    ("Courier Service", "150-300", "100000-300000", "300000-600000", 5000, 0.25, 2),
    ("Mobile Repair", "100-200", "50000-200000", "200000-400000", 4000, 0.40, 1),
    ("Laptop Repair", "150-300", "100000-300000", "300000-600000", 5000, 0.35, 2),
    ("Car Wash", "400-800", "500000-1000000", "1000000-2000000", 15000, 0.35, 4),
    ("Bike Wash", "200-400", "200000-500000", "500000-1000000", 8000, 0.35, 2),
    ("Water Purifier Store", "200-400", "300000-700000", "800000-1500000", 9000, 0.25, 2),
    ("Furniture Store", "1000-2000", "1000000-3000000", "3000000-6000000", 40000, 0.20, 5),
    ("Mattress Store", "500-1000", "500000-1200000", "1500000-2500000", 15000, 0.25, 3),
    ("Interior Design Office", "400-800", "500000-1000000", "1000000-2000000", 20000, 0.35, 4),
    ("Paint Store", "400-900", "400000-1000000", "1500000-2500000", 18000, 0.20, 3),
    ("Tiles Store", "800-1500", "1000000-3000000", "3000000-6000000", 35000, 0.18, 4),
    ("Construction Material Shop", "1000-2000", "800000-2500000", "4000000-7000000", 50000, 0.18, 5),
    ("Pharmacy Franchise", "250-500", "500000-1000000", "1500000-2000000", 15000, 0.20, 3),
    ("Dental Clinic", "400-800", "1500000-4000000", "3000000-6000000", 25000, 0.35, 5),
    ("Diagnostic Lab", "600-1200", "2000000-5000000", "4000000-7000000", 35000, 0.30, 6),
    ("Pathology Lab", "400-800", "1500000-3000000", "3000000-5000000", 25000, 0.30, 5),
    ("Optical Store", "250-500", "300000-800000", "1000000-1500000", 12000, 0.35, 2),
    ("Footwear Store", "400-800", "500000-1200000", "1500000-2500000", 18000, 0.25, 3),
    ("Sports Shop", "400-900", "500000-1500000", "1500000-3000000", 20000, 0.25, 3),
    ("Cycle Store", "400-900", "500000-1200000", "1500000-2500000", 18000, 0.20, 3),
    ("Laptop Showroom", "500-900", "800000-2000000", "2000000-3500000", 30000, 0.15, 3),
    ("Camera Store", "300-700", "500000-1500000", "1500000-3000000", 18000, 0.18, 2),
    ("Drone Store", "300-600", "500000-1200000", "1500000-2500000", 20000, 0.20, 2),
    ("Tattoo Studio", "200-400", "300000-700000", "800000-1500000", 10000, 0.40, 2),
    ("Spa Center", "600-1200", "800000-2000000", "2000000-3500000", 20000, 0.40, 5),
    ("Yoga Studio", "600-1200", "500000-1200000", "1500000-2500000", 15000, 0.35, 3),
    ("Dance Studio", "800-1500", "700000-2000000", "2000000-4000000", 18000, 0.35, 4),
    ("Music Academy", "800-1500", "700000-2000000", "2000000-4000000", 15000, 0.30, 4),
    ("Coaching Center", "800-1500", "500000-1500000", "2000000-4000000", 25000, 0.35, 5),
    ("Play School", "1000-2000", "2000000-4000000", "4000000-7000000", 30000, 0.30, 6),
    ("Daycare Center", "800-1500", "1500000-3000000", "3000000-5000000", 20000, 0.30, 5),
    ("Furniture Repair", "300-600", "200000-500000", "500000-1000000", 7000, 0.30, 2),
    ("AC Repair Shop", "300-600", "200000-600000", "600000-1200000", 8000, 0.35, 2),
    ("Electric Repair Shop", "200-400", "100000-300000", "300000-600000", 6000, 0.35, 2),
    ("Plumbing Service Shop", "200-400", "100000-300000", "300000-600000", 6000, 0.35, 2),
    ("Home Cleaning Service", "200-400", "200000-500000", "500000-1000000", 8000, 0.35, 3),
    ("Car Rental Office", "300-600", "300000-700000", "1000000-2000000", 12000, 0.25, 2),
    ("Bike Rental Shop", "200-400", "200000-500000", "800000-1500000", 8000, 0.30, 2),
    ("Event Planning Office", "300-600", "300000-700000", "800000-1500000", 12000, 0.30, 3),
    ("Wedding Planner Office", "400-800", "500000-1200000", "1500000-2500000", 20000, 0.35, 4),
    ("Party Decoration Store", "300-600", "200000-600000", "600000-1200000", 9000, 0.30, 3),
    ("Balloon Decoration Store", "200-400", "100000-300000", "300000-600000", 6000, 0.30, 2),
    ("Printing Press", "600-1200", "1000000-2500000", "2500000-4000000", 20000, 0.30, 4),
    ("Packaging Store", "400-800", "400000-900000", "1000000-2000000", 12000, 0.25, 3),
    ("Plastic Goods Shop", "400-800", "400000-900000", "1000000-2000000", 15000, 0.22, 3),
    ("Kitchen Equipment Store", "500-900", "700000-1500000", "2000000-3000000", 20000, 0.20, 3),
]


def _build_seed_data():
    """Build FRANCHISE_SEED_DATA from raw CSV data."""
    data = []
    for row in _RAW_DATA:
        name, area_sqft, setup_cost_str, investment_str, avg_daily_rev, margin, employees = row
        sqft_min, sqft_max = _parse_range(area_sqft)
        setup_cost = _parse_range_mid(setup_cost_str)
        investment = _parse_range_mid(investment_str)
        category = CATEGORY_MAP.get(name, "shop")

        # Derive monthly operating cost: (daily_revenue * 30 * (1 - margin)) * 0.85
        # This gives a reasonable operating cost relative to revenue
        monthly_revenue = avg_daily_rev * 30
        monthly_operating_cost = monthly_revenue * (1 - margin) * 0.85

        # Average customer spend derived from daily revenue / estimated daily customers
        # Rough estimate: daily customers = daily_revenue / avg_ticket
        avg_spend_map = {
            "cafe": 150, "restaurant": 300, "fast_food": 250, "bakery": 120,
            "clothing": 1500, "jewelry": 5000, "pharmacy": 400, "salon": 500,
            "gym": 200, "electronics": 2000, "supermarket": 600, "shop": 300,
            "clinic": 800, "education": 2000,
        }
        avg_spend = avg_spend_map.get(category, 300)

        data.append({
            "name": name,
            "category": category,
            "area_sqft_min": sqft_min,
            "area_sqft_max": sqft_max,
            "setup_cost": setup_cost,
            "investment": investment,
            "avg_daily_revenue": avg_daily_rev,
            "avg_customer_spend": avg_spend,
            "employees_required": employees,
            "monthly_operating_cost": round(monthly_operating_cost),
            "profit_margin": round(margin * 100, 1),  # store as percentage
            "min_population": MIN_POPULATION.get(category, 10000),
            "target_demographic": TARGET_DEMOGRAPHICS.get(category, "All demographics"),
        })
    return data


FRANCHISE_SEED_DATA = _build_seed_data()


def seed_franchises():
    """Insert predefined franchise types into the database."""
    existing = FranchiseType.query.count()
    if existing > 0:
        return existing

    for data in FRANCHISE_SEED_DATA:
        franchise = FranchiseType(**data)
        db.session.add(franchise)

    db.session.commit()
    return len(FRANCHISE_SEED_DATA)


def get_all_franchises():
    """Get all franchise types."""
    return [f.to_dict() for f in FranchiseType.query.all()]


def get_franchise_by_id(franchise_id):
    """Get a specific franchise type."""
    f = FranchiseType.query.get(franchise_id)
    return f.to_dict() if f else None


def recommend_franchises(population, working_population, literacy_rate, competitor_data=None):
    """Recommend best franchise types based on area demographics."""
    franchises = FranchiseType.query.all()
    recommendations = []

    for f in franchises:
        score = 0

        # Population threshold
        if population >= f.min_population:
            score += 30
        elif population >= f.min_population * 0.7:
            score += 15

        # Working population ratio (good for B2C)
        work_ratio = working_population / population if population > 0 else 0
        if work_ratio > 0.4:
            score += 20
        elif work_ratio > 0.3:
            score += 10

        # Literacy correlates with spending power
        if literacy_rate > 80:
            score += 20
        elif literacy_rate > 60:
            score += 10

        # Profit margin bonus
        score += f.profit_margin * 0.5

        # Lower setup cost is better for risk-averse
        if f.setup_cost < 1500000:
            score += 10
        elif f.setup_cost < 3000000:
            score += 5

        # Competitor penalty
        if competitor_data:
            direct = competitor_data.get('direct_competitors', 0)
            if direct > 10:
                score -= 15
            elif direct > 5:
                score -= 8

        recommendations.append({
            'franchise': f.to_dict(),
            'score': round(score, 1),
            'reasons': _get_recommendation_reasons(f, population, work_ratio, literacy_rate),
        })

    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations


def _get_recommendation_reasons(franchise, population, work_ratio, literacy_rate):
    """Generate human-readable reasons for the recommendation."""
    reasons = []
    if population >= franchise.min_population:
        reasons.append("Sufficient population base")
    if work_ratio > 0.4:
        reasons.append("High working population ratio")
    if literacy_rate > 75:
        reasons.append("High literacy indicates good spending power")
    if franchise.profit_margin > 25:
        reasons.append("High profit margin potential")
    if franchise.setup_cost < 1500000:
        reasons.append("Low initial investment")
    return reasons
