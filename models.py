"""Modelos e validações do pedido de crédito corporativo."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from config import REQUIRED_FIELDS


@dataclass
class CreditApplication:
    """Representa um pedido de crédito corporativo para análise."""

    company_id: str = ""
    company_name: str = ""
    nif: str = ""
    sector: str = ""
    province: str = ""
    incorporation_date: str = ""
    annual_revenue: float = 0.0
    ebitda: float = 0.0
    net_income: float = 0.0
    total_assets: float = 0.0
    total_liabilities: float = 0.0
    current_assets: float = 0.0
    current_liabilities: float = 0.0
    equity: float = 0.0
    cash: float = 0.0
    accounts_receivable: float = 0.0
    inventory: float = 0.0
    accounts_payable: float = 0.0
    operating_cash_flow: float = 0.0
    capex: float = 0.0
    existing_debt: float = 0.0
    annual_interest_expense: float = 0.0
    annual_debt_service: float = 0.0
    requested_amount: float = 0.0
    requested_term_months: int = 12
    interest_rate: float = 0.0
    currency: str = "AOA"
    purpose: str = ""
    main_customers: str = ""
    top_customer_concentration: float = 0.0
    import_dependency: float = 0.0
    foreign_currency_revenue_percentage: float = 0.0
    foreign_currency_debt_percentage: float = 0.0
    payment_history: float = 0.0
    current_overdue_amount: float = 0.0
    guarantee_type: str = ""
    guarantee_market_value: float = 0.0
    guarantee_liquidation_value: float = 0.0
    guarantee_encumbrance: str = "nenhum"
    management_quality: int = 0
    information_quality: int = 0
    sector_risk: float = 0.0
    circ_status: str = "bom"
    compliance_status: str = "bom"
    documents_complete: bool = True
    expected_drawn_fees: float = 0.0
    loan_limit: float = 0.0
    usage_percentage: float = 100.0

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        missing = []
        for field_name in REQUIRED_FIELDS:
            value = getattr(self, field_name, None)
            if value in (None, "", 0):
                missing.append(field_name)

        if missing:
            raise ValueError(f"Campos obrigatórios em falta: {', '.join(missing)}")

        if self.requested_amount <= 0:
            raise ValueError("O montante solicitado deve ser superior a zero.")
        if self.requested_term_months < 1:
            raise ValueError("O prazo deve ser superior ou igual a 1 mês.")

        for field_name in [
            "annual_revenue",
            "ebitda",
            "net_income",
            "total_assets",
            "total_liabilities",
            "current_assets",
            "current_liabilities",
            "equity",
            "cash",
            "accounts_receivable",
            "inventory",
            "accounts_payable",
            "operating_cash_flow",
            "capex",
            "existing_debt",
            "annual_interest_expense",
            "annual_debt_service",
            "current_overdue_amount",
            "guarantee_market_value",
            "guarantee_liquidation_value",
            "expected_drawn_fees",
            "loan_limit",
            "usage_percentage",
        ]:
            value = getattr(self, field_name, 0)
            if value < 0:
                raise ValueError(f"O campo {field_name} não pode ser negativo.")

        for field_name in [
            "top_customer_concentration",
            "import_dependency",
            "foreign_currency_revenue_percentage",
            "foreign_currency_debt_percentage",
            "payment_history",
            "sector_risk",
        ]:
            value = getattr(self, field_name, 0)
            if not 0 <= value <= 100:
                raise ValueError(f"O campo {field_name} deve estar entre 0 e 100.")

        if self.total_liabilities > self.total_assets:
            raise ValueError("Os passivos excedem os activos totais: rever a consistência do balanço.")
        if self.current_assets > self.total_assets:
            raise ValueError("Os activos correntes não podem exceder os activos totais.")
        if self.current_liabilities > self.total_liabilities:
            raise ValueError("Os passivos correntes não podem exceder os passivos totais.")

        if self.management_quality < 0 or self.management_quality > 100:
            raise ValueError("Qualidade de gestão fora do intervalo aceitável.")
        if self.information_quality < 0 or self.information_quality > 100:
            raise ValueError("Qualidade da informação fora do intervalo aceitável.")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CreditApplication":
        return cls(**payload)
