"""Configurações globais do protótipo."""

from __future__ import annotations

APP_TITLE = "Angola Corporate Credit Decision Engine"
RULES_VERSION = "1.0.0"
CURRENCY_LABEL = "AOA / Kz"
REPORT_WARNING = "Protótipo de apoio à decisão e não substitui o comité de crédito."

SCORE_WEIGHTS = {
    "repayment_capacity": 30,
    "liquidity_profitability": 15,
    "leverage": 15,
    "payment_history": 15,
    "operational_quality": 10,
    "guarantee_quality": 10,
    "management_information": 5,
}

RISK_CLASSES = {
    "A": {"label": "Classe A — baixo risco", "pd": 0.02},
    "B": {"label": "Classe B — risco moderado", "pd": 0.05},
    "C": {"label": "Classe C — risco elevado", "pd": 0.10},
    "D": {"label": "Classe D — risco muito elevado", "pd": 0.20},
    "E": {"label": "Classe E — risco crítico", "pd": 0.40},
}

DEMO_USERS = [
    {"username": "analista", "role": "Analista", "password": "demo123"},
    {"username": "risco", "role": "Risco", "password": "demo123"},
    {"username": "admin", "role": "Administrador", "password": "demo123"},
]

REQUIRED_FIELDS = [
    "company_name",
    "nif",
    "sector",
    "province",
    "annual_revenue",
    "requested_amount",
    "requested_term_months",
    "currency",
    "guarantee_type",
    "purpose",
]
