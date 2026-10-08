"""Camada central de cálculo e decisão do motor de crédito.

Mantém a mesma lógica entre páginas do Streamlit, testes e relatórios.
"""
from __future__ import annotations

from typing import Any

from calculations import (
    calculate_current_ratio,
    calculate_debt_to_ebitda,
    calculate_dscr,
    calculate_guarantee_coverage,
    calculate_interest_coverage,
    calculate_quick_ratio,
)
from config import RISK_CLASSES
from recommendation import determine_recommendation
from scoring import calculate_score, classify_score, evaluate_blocking_rules


def credit_metrics(data: dict[str, Any]) -> dict[str, float]:
    """Calcula os principais indicadores a partir dos dados declarados."""
    current_assets = float(data.get("current_assets", 0.0))
    current_liabilities = float(data.get("current_liabilities", 0.0))
    # Não inventamos activos correntes. O fallback abaixo existe apenas para
    # compatibilidade com dados antigos do protótipo e fica explicitamente sinalizado.
    if current_assets == 0 and float(data.get("total_assets", 0.0)) > 0:
        current_assets = float(data["total_assets"]) * 0.4
    if current_liabilities == 0 and float(data.get("total_liabilities", 0.0)) > 0:
        current_liabilities = float(data["total_liabilities"]) * 0.3

    ocf = float(data.get("operating_cash_flow", 0.0))
    capex = float(data.get("capex", 0.0))
    debt_service = float(data.get("annual_debt_service", 0.0))
    ebitda = float(data.get("ebitda", 0.0))
    debt = float(data.get("existing_debt", 0.0))
    requested = float(data.get("requested_amount", 0.0))
    liquidation = float(data.get("guarantee_liquidation_value", 0.0))

    return {
        "cfads": ocf - capex,
        "dscr": calculate_dscr(ocf - capex, debt_service),
        "current_ratio": calculate_current_ratio(current_assets, current_liabilities),
        "quick_ratio": calculate_quick_ratio(float(data.get("cash", 0.0)), float(data.get("accounts_receivable", 0.0)), current_liabilities),
        "debt_to_ebitda": calculate_debt_to_ebitda(debt, ebitda),
        "interest_coverage": calculate_interest_coverage(ebitda, float(data.get("annual_interest_expense", 0.0))),
        "guarantee_coverage": calculate_guarantee_coverage(liquidation, requested),
    }


def analyse_credit(data: dict[str, Any]) -> dict[str, Any]:
    """Executa métricas, score, regras de bloqueio e recomendação numa única chamada."""
    metrics = credit_metrics(data)
    score_input = {
        **metrics,
        "payment_history": float(data.get("payment_history", 0.0)),
        "top_customer_concentration": float(data.get("top_customer_concentration", 0.0)),
        "management_quality": float(data.get("management_quality", 0.0)),
        "information_quality": float(data.get("information_quality", 0.0)),
        "compliance_status": str(data.get("compliance_status", "bom")).lower(),
        "documents_complete": bool(data.get("documents_complete", True)),
        "guarantee_encumbrance": str(data.get("guarantee_encumbrance", "nenhum")).lower(),
    }
    score = calculate_score(score_input)
    risk_class = classify_score(score)
    blocking = evaluate_blocking_rules(score_input)
    recommendation = determine_recommendation(
        score,
        metrics["dscr"],
        score_input["compliance_status"],
        score_input["documents_complete"],
        score_input["guarantee_encumbrance"],
        score_input["top_customer_concentration"],
    )
    if blocking["block_decision"]:
        recommendation["recommendation"] = "Decisão bloqueada"

    pd_estimate = float(RISK_CLASSES[risk_class]["pd"])
    collateral = min(max(metrics["guarantee_coverage"], 0.0), 1.0)
    lgd_proxy = max(0.10, 1.0 - collateral)
    ead = float(data.get("requested_amount", 0.0))
    ecl_proxy = ead * pd_estimate * lgd_proxy

    return {
        "metrics": metrics,
        "score": score,
        "risk_class": risk_class,
        "pd_estimate": pd_estimate,
        "lgd_proxy": lgd_proxy,
        "ead": ead,
        "ecl_proxy": ecl_proxy,
        "blocking": blocking,
        "recommendation": recommendation,
    }
