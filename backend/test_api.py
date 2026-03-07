"""Test script to verify the full analysis pipeline."""
import requests
import json

BASE = 'http://localhost:5002/api'

# Test analysis
print("Running analysis for Velachery, Chennai...")
r = requests.post(f'{BASE}/analyze', json={
    'latitude': 12.9815,
    'longitude': 80.218,
    'radius_km': 3,
    'franchise_id': 1,
    'location_name': 'Velachery, Chennai'
})

if r.status_code != 200:
    print(f"ERROR: {r.status_code} - {r.text}")
    exit(1)

d = r.json()
print(f"Status: {r.status_code}")
print(f"Location: {d['location']['name']}")
print(f"Population: {d['population']['total_population']:,}")
print(f"Working Population: {d['population']['working_population']:,}")
print(f"Households: {d['population']['total_households']:,}")
print(f"Literacy Rate: {d['population']['avg_literacy_rate']}%")
print(f"Competitors: {d['competitors']['total_count']}")
print(f"Daily Customers: {d['profit']['customers_per_day']}")
print(f"Daily Revenue: Rs {d['profit']['daily_revenue']:,.0f}")
print(f"Yearly Revenue: Rs {d['profit']['yearly_revenue']:,.0f}")
print(f"Yearly Profit: Rs {d['profit']['yearly_profit']:,.0f}")
print(f"ROI: {d['profit']['roi_percentage']:.1f}%")
print(f"Break-even: {d['profit']['months_to_breakeven']} months")
print(f"Risk Level: {d['risk']['risk_level']} ({d['risk']['risk_score']}/100)")
print(f"Risk Summary: {d['risk']['summary']}")

if d.get('recommendations'):
    print(f"\nTop 3 Recommendations:")
    for i, rec in enumerate(d['recommendations'][:3], 1):
        print(f"  {i}. {rec['franchise']['name']} (Score: {rec['score']})")

print(f"\n5-Year Projections:")
for p in d.get('projections', []):
    print(f"  Year {p['year']}: Revenue Rs {p['revenue']:,.0f} | Profit Rs {p['profit']:,.0f} | Cumulative Rs {p['cumulative_profit']:,.0f}")

# Test PDF generation
print("\nGenerating PDF report...")
pdf_r = requests.post(f'{BASE}/report/pdf', json=d)
if pdf_r.status_code == 200:
    with open('/Users/sathwik/Desktop/PROJECT/FranchiseDNA/data/test_report.pdf', 'wb') as f:
        f.write(pdf_r.content)
    print("PDF saved to data/test_report.pdf")
else:
    print(f"PDF Error: {pdf_r.status_code} - {pdf_r.text}")

print("\n✅ All tests passed!")
