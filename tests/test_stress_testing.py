from stress_testing import run_scenarios


def test_stress_scenario_output():
    result = run_scenarios({
        "annual_revenue": 5000000,
        "ebitda": 700000,
        "operating_cash_flow": 400000,
        "capex": 150000,
        "annual_debt_service": 300000,
        "current_assets": 800000,
        "current_liabilities": 500000,
        "existing_debt": 1200000,
        "guarantee_liquidation_value": 900000,
        "requested_amount": 800000,
        "currency": "AOA",
        "foreign_currency_debt_percentage": 0,
    })
    assert set(result.keys()) == {"base", "downside", "severo"}
    assert "dscr" in result["base"]
