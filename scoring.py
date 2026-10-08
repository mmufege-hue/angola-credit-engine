"""Motor de score e regras de decisão do modelo de crédito."""

from __future__ import annotations

from typing import Any

from config import SCORE_WEIGHTS


def score_dscr(dscr: float) -> float:
    if dscr >= 1.5:
        return 100.0
    if 1.25 <= dscr < 1.5:
        return 80.0
    if 1.0 <= dscr < 1.25:
        return 55.0
    return 25.0


def score_liquidity(current_ratio: float) -> float:
    if current_ratio >= 1.5:
        return 100.0
    if 1.0 <= current_ratio < 1.5:
        return 70.0
    return 35.0


def score_debt_to_ebitda(debt_to_ebitda: float) -> float:
    if debt_to_ebitda <= 2.0:
        return 100.0
    if debt_to_ebitda <= 3.5:
        return 75.0
    if debt_to_ebitda <= 5.0:
        return 50.0
    return 25.0


def score_customer_concentration(top_customer_concentration: float) -> float:
    if top_customer_concentration <= 20:
        return 100.0
    if top_customer_concentration <= 40:
        return 70.0
    return 35.0


def score_payment_history(payment_history: float) -> float:
    if payment_history >= 90:
        return 100.0
    if payment_history >= 75:
        return 80.0
    if payment_history >= 60:
        return 60.0
    return 30.0


def score_operation_quality(quality: float) -> float:
    return min(max(quality, 0), 100)


def score_guarantee_quality(guarantee_coverage: float) -> float:
    if guarantee_coverage >= 1.0:
        return 100.0
    if guarantee_coverage >= 0.8:
        return 75.0
    if guarantee_coverage >= 0.6:
        return 55.0
    return 30.0


def score_management_quality(management_quality: float, information_quality: float) -> float:
    return (management_quality + information_quality) / 2.0


def calculate_score(data: dict[str, Any]) -> float:
    """Calcula score com receita de 0 a 100."""
    dscr = float(data.get("dscr", 0.0))
    current_ratio = float(data.get("current_ratio", 0.0))
    debt_to_ebitda = float(data.get("debt_to_ebitda", 0.0))
    payment_history = float(data.get("payment_history", 0.0))
    top_customer_concentration = float(data.get("top_customer_concentration", 0.0))
    guarantee_coverage = float(data.get("guarantee_coverage", 0.0))
    management_quality = float(data.get("management_quality", 0.0))
    information_quality = float(data.get("information_quality", 0.0))

    score_component = {
        "repayment_capacity": score_dscr(dscr) * (SCORE_WEIGHTS["repayment_capacity"] / 100.0),
        "liquidity_profitability": score_liquidity(current_ratio) * (SCORE_WEIGHTS["liquidity_profitability"] / 100.0),
        "leverage": score_debt_to_ebitda(debt_to_ebitda) * (SCORE_WEIGHTS["leverage"] / 100.0),
        "payment_history": score_payment_history(payment_history) * (SCORE_WEIGHTS["payment_history"] / 100.0),
        "operational_quality": score_customer_concentration(top_customer_concentration) * (SCORE_WEIGHTS["operational_quality"] / 100.0),
        "guarantee_quality": score_guarantee_quality(guarantee_coverage) * (SCORE_WEIGHTS["guarantee_quality"] / 100.0),
        "management_information": score_management_quality(management_quality, information_quality) * (SCORE_WEIGHTS["management_information"] / 100.0),
    }

    weighted_total = sum(score_component.values())
    return round(min(max(weighted_total, 0.0), 100.0), 2)


def classify_score(score: float) -> str:
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    if score >= 35:
        return "D"
    return "E"


def evaluate_blocking_rules(data: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    blocked = False

    if not data.get("documents_complete", True):
        reasons.append("Documentação essencial incompleta.")
        blocked = True
    compliance = str(data.get("compliance_status", "bom")).lower()
    if compliance in {"risco", "critico"}:
        reasons.append("Risco de compliance exige revisão.")
        blocked = True
    elif compliance == "atencao":
        reasons.append("Compliance em atenção: reforçar validação documental e controlo pré-aprovação.")
    if str(data.get("guarantee_encumbrance", "nenhum")).lower() in {"incerto", "onus desconhecido"}:
        reasons.append("Garantia com ónus não esclarecido.")
        blocked = True
    if float(data.get("dscr", 0.0)) < 1.0:
        reasons.append("DSCR abaixo de 1,0x exige reestruturação ou rejeição.")
        blocked = True

    return {"block_decision": blocked, "reasons": reasons}
