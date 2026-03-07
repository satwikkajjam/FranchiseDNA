import React, { useState, useMemo } from 'react';

function formatCurrency(amount) {
  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(2)} Cr`;
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(2)} L`;
  if (amount >= 1000) return `₹${(amount / 1000).toFixed(1)}K`;
  return `₹${Math.round(amount).toLocaleString()}`;
}

const CATEGORIES = {
  "Food & Beverage": ["Coffee Shop", "Juice Point", "Tea Shop", "Food Center", "Tiffin Center", "Bakery", "Ice Cream Shop", "Sweet Shop", "Fast Food Outlet", "Pizza Shop", "Restaurant", "Cloud Kitchen"],
  "Retail & Shopping": ["Clothing Store", "Gold Shop", "Supermarket", "Footwear Store", "Organic Store", "Gift Shop", "Perfume Shop", "Watch Store", "Toy Store", "Book Store", "Stationery Store", "Sports Shop", "Pet Shop", "Flower Shop"],
  "Electronics & Tech": ["Mobile Store", "Electronics Store", "Computer Store", "Laptop Showroom", "Camera Store", "Drone Store", "Internet Cafe", "Gaming Cafe"],
  "Health & Medical": ["Medical Store", "Pharmacy Franchise", "Dental Clinic", "Diagnostic Lab", "Pathology Lab", "Optical Store"],
  "Beauty & Wellness": ["Salon", "Tattoo Studio", "Spa Center"],
  "Fitness & Sports": ["Gym", "Yoga Studio", "Dance Studio", "Cycle Store"],
  "Education": ["Coaching Center", "Music Academy", "Play School", "Daycare Center"],
  "Food Markets": ["Vegetable Market", "Meat Shop", "Fish Market"],
  "Home & Construction": ["Furniture Store", "Mattress Store", "Interior Design Office", "Paint Store", "Tiles Store", "Construction Material Shop", "Hardware Store", "Kitchen Equipment Store", "Water Purifier Store"],
  "Automobile": ["Car Accessories", "Bike Service", "Car Wash", "Bike Wash", "Car Rental Office", "Bike Rental Shop"],
  "Repair & Services": ["Mobile Repair", "Laptop Repair", "Furniture Repair", "AC Repair Shop", "Electric Repair Shop", "Plumbing Service Shop", "Laundry Shop", "Dry Cleaning", "Home Cleaning Service"],
  "Events & Media": ["Photography Studio", "Event Planning Office", "Wedding Planner Office", "Party Decoration Store", "Balloon Decoration Store", "Printing Press", "Photocopy Shop"],
  "Logistics & Travel": ["Travel Agency", "Courier Service", "Packaging Store"],
  "Others": ["Plastic Goods Shop"],
};

function FranchiseSelector({ franchises, selected, onChange }) {
  const [search, setSearch] = useState('');
  const [expandedCat, setExpandedCat] = useState(null);

  const filtered = useMemo(() => {
    if (!search.trim()) return null;
    const q = search.toLowerCase();
    return franchises.filter(f => f.name.toLowerCase().includes(q));
  }, [search, franchises]);

  const franchiseByName = useMemo(() => {
    const map = {};
    franchises.forEach(f => { map[f.name] = f; });
    return map;
  }, [franchises]);

  const handleSelect = (f) => {
    onChange(f);
    setSearch('');
  };

  return (
    <div className="franchise-selector">
      <h3>Store Type</h3>
      <input
        type="text"
        className="franchise-search"
        placeholder="Search 90 store types..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {filtered && filtered.length > 0 && (
        <div className="franchise-dropdown">
          {filtered.slice(0, 10).map(f => (
            <div
              key={f.id}
              className={`franchise-option ${selected?.id === f.id ? 'active' : ''}`}
              onClick={() => handleSelect(f)}
            >
              {f.name}
              <span className="option-cost">{formatCurrency(f.setup_cost)}</span>
            </div>
          ))}
          {filtered.length > 10 && (
            <div className="franchise-option muted">...and {filtered.length - 10} more</div>
          )}
        </div>
      )}

      {!search && (
        <div className="category-list">
          {Object.entries(CATEGORIES).map(([cat, names]) => (
            <div key={cat} className="category-group">
              <div
                className={`category-header ${expandedCat === cat ? 'expanded' : ''}`}
                onClick={() => setExpandedCat(expandedCat === cat ? null : cat)}
              >
                <span>{cat}</span>
                <span className="cat-count">{names.length}</span>
              </div>
              {expandedCat === cat && (
                <div className="category-items">
                  {names.map(name => {
                    const f = franchiseByName[name];
                    if (!f) return null;
                    return (
                      <div
                        key={f.id}
                        className={`franchise-option ${selected?.id === f.id ? 'active' : ''}`}
                        onClick={() => handleSelect(f)}
                      >
                        {f.name}
                        <span className="option-cost">{formatCurrency(f.setup_cost)}</span>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {selected && (
        <div className="franchise-details">
          <div className="selected-name">{selected.name}</div>
          <div className="detail-grid">
            <p>Setup: <strong>{formatCurrency(selected.setup_cost)}</strong></p>
            <p>Investment: <strong>{formatCurrency(selected.investment)}</strong></p>
            <p>Margin: <strong>{selected.profit_margin}%</strong></p>
            <p>Staff: <strong>{selected.employees_required}</strong></p>
            <p>Area: <strong>{selected.area_sqft || 'N/A'} sqft</strong></p>
            <p>Daily Rev: <strong>{formatCurrency(selected.avg_daily_revenue)}</strong></p>
          </div>
        </div>
      )}
    </div>
  );
}

export default FranchiseSelector;
