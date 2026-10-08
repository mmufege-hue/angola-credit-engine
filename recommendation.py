"""Motor de recomendação de crédito e condições."""

from __future__ import annotations

from typing import Any


def determine_recommendation(score: float, dscr: float, compliance_status: str, documents_complete: bool, guarantee_encumbrance: str, concentration: float) -> dict[str, Any]:
    """Retorna recomendação final com condições e rationale."""
    positive = []
    negative = []
    alerts = []
    conditions = []
    missing = []

    if dscr >= 1.25:
        positive.append(f"DSCR de {dscr:.2f}x.")
    else:
        negative.append(f"DSCR de {dscr:.2f}x abaixo do conforto mínimo.")
    if score >= 65:
        positive.append("Score de risco dentro do intervalo aceitável.")
    else:
        negative.append("Score de risco fraco para aprovação sem mitigantes.")
    compliance = compliance_status.lower()
    if compliance in {"risco", "critico"}:
        alerts.append("Existe risco de compliance relevante.")
    elif compliance == "atencao":
        alerts.append("Compliance em atenção: solicitar confirmação documental adicional antes da decisão final.")
    if not documents_complete:
        missing.append("Documentação essencial incompleta.")
    if guarantee_encumbrance.lower() in {"incerto", "onus desconhecido"}:
        alerts.append("Garantia com ónus não esclarecidos.")
    if concentration > 40:
        negative.append(f"Concentração do principal cliente em {concentration:.0f}%.")
        conditions.append("Mitigar concentração com reforço de garantias ou diversificação de clientes.")

    if not documents_complete:
        recommendation = "Solicitar informação adicional"
    elif compliance_status.lower() in {"risco", "critico"}:
        recommendation = "Enviar para comité"
    elif compliance_status.lower() == "atencao":
        recommendation = "Aprovar com condições"
    elif dscr < 1.0:
        recommendation = "Reestruturar"
    elif guarantee_encumbrance.lower() in {"incerto", "onus desconhecido"}:
        recommendation = "Solicitar informação adicional"
    elif score >= 80:
        recommendation = "Aprovar"
    elif score >= 65:
        recommendation = "Aprovar com condições"
    elif score >= 50:
        recommendation = "Enviar para comité"
    elif score >= 35:
        recommendation = "Reestruturar"
    else:
        recommendation = "Rejeitar"

    if score >= 65 and dscr >= 1.25 and not missing and compliance_status.lower() in {"bom", "atencao"}:
        conditions.extend([
            "Domiciliar receitas no banco.",
            "Entregar demonstrações financeiras trimestrais.",
            "Rever o DSCR trimestralmente.",
        ])

    return {
        "recommendation": recommendation,
        "positive_factors": positive,
        "negative_factors": negative,
        "alerts": alerts,
        "conditions": conditions,
        "missing_data": missing,
    }
