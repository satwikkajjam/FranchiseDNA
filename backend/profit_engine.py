"""
Profit Prediction Engine - Estimates revenue and profit for a franchise at a location.
"""

BANK_FD_RATE = 0.075  # 7.5% annual FD interest rate


def predict_profit(population_data, franchise_data, competitor_count):
    """
    Estimate profit using the franchise's avg_daily_revenue as baseline,
    adjusted by population density and competition.
    Operating costs scale proportionally with revenue so that the franchise's
    inherent profit margin is respected regardless of location size.
    """
    population = population_data.get('total_population', 0)
    working_pop = population_data.get('working_population', 0)

    setup_cost = franchise_data.get('setup_cost', 0)
    investment = franchise_data.get('investment', setup_cost)
    avg_spend = franchise_data.get('avg_customer_spend', 0)
    profit_margin = franchise_data.get('profit_margin', 15) / 100
    base_daily_revenue = franchise_data.get('avg_daily_revenue', 0)

    # --- Population multiplier ---
    pop_multiplier = min(max(population / 50000, 0.4), 3.0)

    # --- Competition factor ---
    if competitor_count > 15:
        competition_factor = 0.55
    elif competitor_count > 10:
        competition_factor = 0.65
    elif competitor_count > 5:
        competition_factor = 0.75
    elif competitor_count > 2:
        competition_factor = 0.88
    else:
        competition_factor = 1.0

    # --- Working population bonus ---
    work_ratio = working_pop / population if population > 0 else 0.4
    work_bonus = 1 + (work_ratio - 0.3) * 0.3

    # --- Adjusted daily revenue ---
    daily_revenue = base_daily_revenue * pop_multiplier * competition_factor * work_bonus
    customers_per_day = int(daily_revenue / avg_spend) if avg_spend > 0 else 0

    # --- Yearly calculations ---
    operating_days = 330
    yearly_revenue = daily_revenue * operating_days

    # Operating costs scale with revenue (margin-based)
    # This ensures profit margin is naturally respected at any scale
    yearly_operating_cost = yearly_revenue * (1 - profit_margin)

    setup_amortization = setup_cost / 3  # 3-year amortization
    total_yearly_expenses = yearly_operating_cost + setup_amortization

    yearly_profit = yearly_revenue - total_yearly_expenses
    actual_margin = (yearly_profit / yearly_revenue * 100) if yearly_revenue > 0 else 0

    # Break-even
    total_investment = investment if investment else setup_cost
    monthly_net = (yearly_revenue * profit_margin) / 12
    months_to_breakeven = (
        int(total_investment / monthly_net) if monthly_net > 0 else -1
    )

    roi = (yearly_profit / total_investment * 100) if total_investment > 0 else 0

    # --- Bank interest comparison ---
    bank_yearly_interest = total_investment * BANK_FD_RATE

    return {
        'customers_per_day': customers_per_day,
        'daily_revenue': round(daily_revenue, 2),
        'yearly_revenue': round(yearly_revenue, 2),
        'yearly_operating_cost': round(yearly_operating_cost, 2),
        'setup_amortization_yearly': round(setup_amortization, 2),
        'total_yearly_expenses': round(total_yearly_expenses, 2),
        'yearly_profit': round(yearly_profit, 2),
        'actual_profit_margin': round(actual_margin, 2),
        'monthly_revenue': round(yearly_revenue / 12, 2),
        'monthly_expenses': round(total_yearly_expenses / 12, 2),
        'months_to_breakeven': months_to_breakeven,
        'roi_percentage': round(roi, 2),
        'competition_factor': competition_factor,
        'pop_multiplier': round(pop_multiplier, 2),
        'total_investment': total_investment,
        'bank_fd_rate': BANK_FD_RATE * 100,
        'bank_yearly_interest': round(bank_yearly_interest, 2),
        'franchise_vs_bank': round(yearly_profit - bank_yearly_interest, 2),
    }


def generate_projections(profit_data, years=5):
    """Generate year-over-year projections with growth + bank interest comparison."""
    projections = []
    yearly_revenue = profit_data['yearly_revenue']
    yearly_operating_cost = profit_data['yearly_operating_cost']
    setup_cost = profit_data.get('setup_amortization_yearly', 0) * 3
    total_investment = profit_data.get('total_investment', setup_cost)

    cumulative_franchise = -total_investment
    cumulative_bank = 0
    growth_rate = 0.08  # 8% revenue growth
    cost_inflation = 0.05  # 5% cost inflation

    for year in range(1, years + 1):
        rev = yearly_revenue * (1 + growth_rate) ** (year - 1)
        op_cost = yearly_operating_cost * (1 + cost_inflation) ** (year - 1)
        amort = setup_cost / 3 if year <= 3 else 0
        expenses = op_cost + amort
        profit = rev - expenses
        cumulative_franchise += profit

        # Bank FD: compound interest on total investment
        bank_value = total_investment * (1 + BANK_FD_RATE) ** year
        bank_interest_this_year = (
            total_investment * (1 + BANK_FD_RATE) ** year
            - total_investment * (1 + BANK_FD_RATE) ** (year - 1)
        )
        cumulative_bank = bank_value - total_investment

        projections.append({
            'year': year,
            'revenue': round(rev, 2),
            'expenses': round(expenses, 2),
            'profit': round(profit, 2),
            'cumulative_profit': round(cumulative_franchise, 2),
            'bank_interest': round(bank_interest_this_year, 2),
            'cumulative_bank': round(cumulative_bank, 2),
            'growth_applied': f"{growth_rate * 100}%",
        })

    return projections
