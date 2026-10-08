"""Cenários de stress e sensibilidade do crédito."""

from __future__ import annotations

from typing import Any

from calculations import (
    calculate_current_ratio,
    calculate_debt_to_ebitda,
    calculate_dscr,
    calculate_guarantee_coverage,
)


def run_scenarios(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Executa os cenários base, downside e severo."""
    revenue = float(data.get("annual_revenue", 0.0))
    ebitda = float(data.get("ebitda", 0.0))
    operating_cash_flow = float(data.get("operating_cash_flow", 0.0))
    capex = float(data.get("capex", 0.0))
    annual_debt_service = float(data.get("annual_debt_service", 0.0))
    current_assets = float(data.get("current_assets", 0.0)) or float(data.get("total_assets", 0.0)) * 0.4
    current_liabilities = float(data.get("current_liabilities", 0.0)) or float(data.get("total_liabilities", 0.0)) * 0.3
    existing_debt = float(data.get("existing_debt", 0.0))
    guarantee_liquidation_value = float(data.get("guarantee_liquidation_value", 0.0))
    requested_amount = float(data.get("requested_amount", 0.0))
    rate = float(data.get("interest_rate", 0.0))
    fx_debt_pct = float(data.get("foreign_currency_debt_percentage", 0.0))
    currency = str(data.get("currency", "AOA")).upper()

    base = {
        "revenue": revenue,
        "ebitda": ebitda,
        "operating_cash_flow": operating_cash_flow,
        "debt_service": annual_debt_service,
        "dscr": calculate_dscr(operating_cash_flow - capex, annual_debt_service),
        "current_ratio": calculate_current_ratio(current_assets, current_liabilities),
        "debt_to_ebitda": calculate_debt_to_ebitda(existing_debt, ebitda),
        "guarantee_coverage": calculate_guarantee_coverage(guarantee_liquidation_value, requested_amount),
        "decision": "Aprovar com condições",
    }

    downside_revenue = revenue * 0.85
    downside_ebitda = ebitda * 0.80
    downside_cash_flow = operating_cash_flow * 0.80
    downside_service = annual_debt_service * (1 + 0.02)
    downside_dscr = calculate_dscr(downside_cash_flow - capex, downside_service)
    downside = {
        "revenue": downside_revenue,
        "ebitda": downside_ebitda,
        "operating_cash_flow": downside_cash_flow,
        "debt_service": downside_service,
        "dscr": downside_dscr,
        "current_ratio": calculate_current_ratio(current_assets * 0.95, current_liabilities * 1.05),
        "debt_to_ebitda": calculate_debt_to_ebitda(existing_debt * 1.05, downside_ebitda),
        "guarantee_coverage": calculate_guarantee_coverage(guarantee_liquidation_value * 0.92, requested_amount),
        "decision": "Enviar para comité" if downside_dscr < 1.0 else "Reestruturar",
    }

    severe_revenue = revenue * 0.70
    severe_ebitda = ebitda * 0.60
    severe_cash_flow = operating_cash_flow * 0.60
    severe_rate = rate + 5.0
    # Heurística: +5 p.p. de taxa traduzidos num aumento de 20% do serviço.
    # O cálculo definitivo deve usar o cronograma de amortização real.
    severe_service = annual_debt_service * 1.20
    severe_dscr = calculate_dscr(severe_cash_flow - capex, severe_service)
    severe_guarantee_value = guarantee_liquidation_value * 0.80
    severe_fx_adjustment = 1.0 - 0.25 if fx_debt_pct > 0 and currency != "AOA" else 1.0
    severe = {
        "revenue": severe_revenue,
        "ebitda": severe_ebitda,
        "operating_cash_flow": severe_cash_flow,
        "debt_service": severe_service,
        "dscr": severe_dscr,
        "current_ratio": calculate_current_ratio(current_assets * 0.80, current_liabilities * 1.10),
        "debt_to_ebitda": calculate_debt_to_ebitda(existing_debt * 1.10, severe_ebitda),
        "guarantee_coverage": calculate_guarantee_coverage(severe_guarantee_value * severe_fx_adjustment, requested_amount),
        "decision": "Rejeitar",
    }

    return {"base": base, "downside": downside, "severo": severe}
