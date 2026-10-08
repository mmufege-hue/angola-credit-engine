import math

from calculations import (
    calculate_current_ratio,
    calculate_quick_ratio,
    calculate_dscr,
    calculate_debt_to_ebitda,
    calculate_ltv,
    calculate_guarantee_coverage,
)


def test_dscr_calculation():
    assert math.isclose(calculate_dscr(120000, 80000), 1.5, rel_tol=1e-9)
    assert math.isclose(calculate_dscr(90000, 120000), 0.75, rel_tol=1e-9)


def test_liquidity_calculation():
    assert math.isclose(calculate_current_ratio(200000, 100000), 2.0, rel_tol=1e-9)
    assert math.isclose(calculate_quick_ratio(150000, 50000, 100000), 2.0, rel_tol=1e-9)


def test_debt_to_ebitda():
    assert math.isclose(calculate_debt_to_ebitda(500000, 250000), 2.0, rel_tol=1e-9)


def test_ltv_and_coverage():
    assert math.isclose(calculate_ltv(400000, 500000), 0.8, rel_tol=1e-9)
    assert math.isclose(calculate_guarantee_coverage(500000, 400000), 1.25, rel_tol=1e-9)


def test_missing_data_handled():
    assert calculate_dscr(0, 0) == 0.0
    assert calculate_current_ratio(0, 0) == 0.0
