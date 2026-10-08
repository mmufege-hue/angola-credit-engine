"""Cálculos financeiros transparentes para análise de crédito."""

from __future__ import annotations


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divide com proteção para valores nulos ou inválidos."""
    if denominator in (None, 0):
        return default
    return float(numerator) / float(denominator)


def calculate_current_ratio(current_assets: float, current_liabilities: float) -> float:
    return safe_divide(current_assets, current_liabilities)


def calculate_quick_ratio(cash: float, accounts_receivable: float, current_liabilities: float) -> float:
    return safe_divide(cash + accounts_receivable, current_liabilities)


def calculate_ebitda_margin(ebitda: float, annual_revenue: float) -> float:
    return safe_divide(ebitda, annual_revenue)


def calculate_net_margin(net_income: float, annual_revenue: float) -> float:
    return safe_divide(net_income, annual_revenue)


def calculate_debt_to_ebitda(existing_debt: float, ebitda: float) -> float:
    return safe_divide(existing_debt, ebitda)


def calculate_debt_to_equity(existing_debt: float, equity: float) -> float:
    return safe_divide(existing_debt, equity)


def calculate_interest_coverage(ebitda: float, annual_interest_expense: float) -> float:
    return safe_divide(ebitda, annual_interest_expense)


def calculate_dscr(cash_flow_available_for_debt_service: float, annual_debt_service: float) -> float:
    return safe_divide(cash_flow_available_for_debt_service, annual_debt_service)


def calculate_receivable_days(accounts_receivable: float, annual_revenue: float) -> float:
    return safe_divide(accounts_receivable, annual_revenue) * 365.0


def estimate_cogs(annual_revenue: float, gross_margin: float) -> float:
    if annual_revenue <= 0:
        return 0.0
    return annual_revenue * (1 - gross_margin)


def calculate_inventory_days(inventory: float, cost_of_goods_sold: float) -> float:
    return safe_divide(inventory, cost_of_goods_sold) * 365.0


def calculate_payable_days(accounts_payable: float, cost_of_goods_sold: float) -> float:
    return safe_divide(accounts_payable, cost_of_goods_sold) * 365.0


def calculate_ltv(requested_amount: float, guarantee_liquidation_value: float) -> float:
    if guarantee_liquidation_value in (None, 0):
        return 0.0
    return safe_divide(requested_amount, guarantee_liquidation_value)


def calculate_guarantee_coverage(guarantee_liquidation_value: float, requested_amount: float) -> float:
    if requested_amount in (None, 0):
        return 0.0
    return safe_divide(guarantee_liquidation_value, requested_amount)
