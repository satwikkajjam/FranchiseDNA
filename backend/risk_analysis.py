"""
Risk Analysis Module - Evaluates risk level of opening a franchise at a location.
"""


def analyze_risk(population_data, franchise_data, competitor_data, profit_data):
    """
    Calculate risk level based on multiple factors.

    Factors:
        1. Competition intensity (high competitors = high risk)
        2. Population density (low density = high risk)
        3. Investment size (high cost = high risk)
        4. Profit margin health
        5. Break-even timeline
        6. Working population ratio
        7. Literacy rate (proxy for spending power)
    """
    risk_factors = []
    total_score = 0  # Higher score = higher risk (0-100)

    # 1. Competition Risk (0-25 points)
    competitor_count = competitor_data.get('total_count', 0)
    direct_competitors = competitor_data.get('direct_competitors', 0)

    if direct_competitors > 15:
        comp_risk = 25
        comp_label = "Very High Competition"
    elif direct_competitors > 10:
        comp_risk = 20
        comp_label = "High Competition"
    elif direct_competitors > 5:
        comp_risk = 12
        comp_label = "Moderate Competition"
    elif direct_competitors > 2:
        comp_risk = 6
        comp_label = "Low Competition"
    else:
        comp_risk = 2
        comp_label = "Minimal Competition"

    risk_factors.append({
        'factor': 'Competition',
        'score': comp_risk,
        'max_score': 25,
        'detail': f"{direct_competitors} direct competitors - {comp_label}",
        'level': _score_to_level(comp_risk, 25),
    })
    total_score += comp_risk

    # 2. Population Risk (0-20 points)
    population = population_data.get('total_population', 0)
    min_pop = franchise_data.get('min_population', 10000)

    if population < min_pop * 0.5:
        pop_risk = 20
        pop_label = "Critically Low Population"
    elif population < min_pop:
        pop_risk = 14
        pop_label = "Below Minimum Population"
    elif population < min_pop * 2:
        pop_risk = 7
        pop_label = "Adequate Population"
    else:
        pop_risk = 2
        pop_label = "Strong Population Base"

    risk_factors.append({
        'factor': 'Population',
        'score': pop_risk,
        'max_score': 20,
        'detail': f"Population {population:,} vs minimum {min_pop:,} - {pop_label}",
        'level': _score_to_level(pop_risk, 20),
    })
    total_score += pop_risk

    # 3. Investment Risk (0-20 points)
    setup_cost = franchise_data.get('setup_cost', 0)
    if setup_cost > 4000000:
        inv_risk = 18
        inv_label = "Very High Investment"
    elif setup_cost > 2500000:
        inv_risk = 13
        inv_label = "High Investment"
    elif setup_cost > 1000000:
        inv_risk = 7
        inv_label = "Moderate Investment"
    else:
        inv_risk = 3
        inv_label = "Low Investment"

    risk_factors.append({
        'factor': 'Investment',
        'score': inv_risk,
        'max_score': 20,
        'detail': f"Setup cost ₹{setup_cost:,.0f} - {inv_label}",
        'level': _score_to_level(inv_risk, 20),
    })
    total_score += inv_risk

    # 4. Profitability Risk (0-20 points)
    roi = profit_data.get('roi_percentage', 0)
    breakeven = profit_data.get('months_to_breakeven', -1)

    if roi < 0 or breakeven < 0:
        profit_risk = 20
        profit_label = "Negative Returns Expected"
    elif roi < 10:
        profit_risk = 15
        profit_label = "Low ROI"
    elif roi < 25:
        profit_risk = 8
        profit_label = "Moderate ROI"
    else:
        profit_risk = 3
        profit_label = "Strong ROI"

    risk_factors.append({
        'factor': 'Profitability',
        'score': profit_risk,
        'max_score': 20,
        'detail': f"ROI {roi:.1f}%, Break-even {breakeven} months - {profit_label}",
        'level': _score_to_level(profit_risk, 20),
    })
    total_score += profit_risk

    # 5. Demographics Risk (0-15 points)
    literacy_rate = population_data.get('avg_literacy_rate', 70)
    work_ratio = (
        population_data.get('working_population', 0) /
        population_data.get('total_population', 1)
    ) if population_data.get('total_population', 0) > 0 else 0.4

    demo_risk = 0
    if literacy_rate < 50:
        demo_risk += 8
    elif literacy_rate < 70:
        demo_risk += 4

    if work_ratio < 0.3:
        demo_risk += 7
    elif work_ratio < 0.4:
        demo_risk += 3

    demo_label = f"Literacy {literacy_rate:.1f}%, Working ratio {work_ratio:.1%}"

    risk_factors.append({
        'factor': 'Demographics',
        'score': min(demo_risk, 15),
        'max_score': 15,
        'detail': demo_label,
        'level': _score_to_level(min(demo_risk, 15), 15),
    })
    total_score += min(demo_risk, 15)

    # Overall risk level
    if total_score >= 65:
        risk_level = "High"
        recommendation = "Not recommended. High risk factors suggest significant potential for loss."
    elif total_score >= 40:
        risk_level = "Medium"
        recommendation = "Proceed with caution. Some risk factors need mitigation."
    else:
        risk_level = "Low"
        recommendation = "Favorable conditions. Good potential for success."

    return {
        'risk_score': total_score,
        'max_possible_score': 100,
        'risk_level': risk_level,
        'risk_percentage': total_score,
        'risk_factors': risk_factors,
        'recommendation': recommendation,
        'summary': _generate_risk_summary(risk_factors, risk_level),
    }


def _score_to_level(score, max_score):
    """Convert a score to Low/Medium/High."""
    ratio = score / max_score if max_score > 0 else 0
    if ratio >= 0.65:
        return "High"
    elif ratio >= 0.35:
        return "Medium"
    return "Low"


def _generate_risk_summary(risk_factors, overall_level):
    """Generate a human-readable risk summary."""
    high_risks = [f for f in risk_factors if f['level'] == 'High']
    medium_risks = [f for f in risk_factors if f['level'] == 'Medium']

    summary = f"Overall Risk: {overall_level}. "
    if high_risks:
        names = ", ".join(f['factor'] for f in high_risks)
        summary += f"High risk in: {names}. "
    if medium_risks:
        names = ", ".join(f['factor'] for f in medium_risks)
        summary += f"Moderate risk in: {names}. "
    if not high_risks and not medium_risks:
        summary += "All factors within acceptable range. "

    return summary
