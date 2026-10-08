"""Página de entrada do pedido de crédito."""
from __future__ import annotations

import streamlit as st

from config import APP_TITLE
from database import save_application, save_company, save_audit_event
from models import CreditApplication
from sample_data import build_demo_form, load_demo_companies
from ui_helpers import apply_global_theme

apply_global_theme()
st.title("1. Entrada do Pedido")
st.caption("Protótipo de apoio à decisão. Use apenas dados fictícios neste ambiente de demonstração.")

if "company_data" not in st.session_state:
    st.session_state.company_data = build_demo_form()

company_data = st.session_state.company_data

c1, c2 = st.columns(2)
with c1:
    if st.button("Carregar empresa de demonstração", use_container_width=True):
        st.session_state.company_data = load_demo_companies()[0].copy()
        st.rerun()
with c2:
    if st.button("Limpar formulário", use_container_width=True):
        st.session_state.company_data = {}
        st.rerun()

with st.form("credit_form"):
    st.subheader("Identificação e pedido")
    a, b, c = st.columns(3)
    with a:
        company_name = st.text_input("Nome da empresa", value=str(company_data.get("company_name", "")))
        nif = st.text_input("NIF", value=str(company_data.get("nif", "")))
        sector = st.text_input("Sector", value=str(company_data.get("sector", "")))
    with b:
        province = st.text_input("Província", value=str(company_data.get("province", "")))
        incorporation_date = st.text_input("Data de constituição", value=str(company_data.get("incorporation_date", "")))
        purpose = st.text_input("Finalidade do crédito", value=str(company_data.get("purpose", "")))
    with c:
        currency = st.selectbox("Moeda", ["AOA", "USD", "EUR"], index=["AOA", "USD", "EUR"].index(str(company_data.get("currency", "AOA")).upper()))
        requested_amount = st.number_input("Montante solicitado", min_value=0.0, value=float(company_data.get("requested_amount", 0.0)), step=10000.0)
        requested_term_months = st.number_input("Prazo (meses)", min_value=1, value=int(company_data.get("requested_term_months", 12)), step=1)
        interest_rate = st.number_input("Taxa anual (%)", min_value=0.0, value=float(company_data.get("interest_rate", 0.0)), step=0.25)

    st.subheader("Demonstrações financeiras")
    a, b, c = st.columns(3)
    with a:
        annual_revenue = st.number_input("Receita anual", min_value=0.0, value=float(company_data.get("annual_revenue", 0.0)))
        ebitda = st.number_input("EBITDA", min_value=0.0, value=float(company_data.get("ebitda", 0.0)))
        net_income = st.number_input("Resultado líquido", min_value=0.0, value=float(company_data.get("net_income", 0.0)))
        operating_cash_flow = st.number_input("Fluxo de caixa operacional", min_value=0.0, value=float(company_data.get("operating_cash_flow", 0.0)))
    with b:
        total_assets = st.number_input("Activos totais", min_value=0.0, value=float(company_data.get("total_assets", 0.0)))
        current_assets = st.number_input("Activos correntes", min_value=0.0, value=float(company_data.get("current_assets", 0.0)))
        cash = st.number_input("Caixa e equivalentes", min_value=0.0, value=float(company_data.get("cash", 0.0)))
        accounts_receivable = st.number_input("Clientes / contas a receber", min_value=0.0, value=float(company_data.get("accounts_receivable", 0.0)))
    with c:
        total_liabilities = st.number_input("Passivos totais", min_value=0.0, value=float(company_data.get("total_liabilities", 0.0)))
        current_liabilities = st.number_input("Passivos correntes", min_value=0.0, value=float(company_data.get("current_liabilities", 0.0)))
        equity = st.number_input("Capital próprio", min_value=0.0, value=float(company_data.get("equity", 0.0)))
        existing_debt = st.number_input("Dívida financeira existente", min_value=0.0, value=float(company_data.get("existing_debt", 0.0)))

    a, b, c = st.columns(3)
    with a:
        annual_interest_expense = st.number_input("Juros anuais", min_value=0.0, value=float(company_data.get("annual_interest_expense", 0.0)))
        annual_debt_service = st.number_input("Serviço anual da dívida", min_value=0.0, value=float(company_data.get("annual_debt_service", 0.0)))
    with b:
        capex = st.number_input("Capex anual", min_value=0.0, value=float(company_data.get("capex", 0.0)))
        inventory = st.number_input("Inventário", min_value=0.0, value=float(company_data.get("inventory", 0.0)))
    with c:
        accounts_payable = st.number_input("Fornecedores / contas a pagar", min_value=0.0, value=float(company_data.get("accounts_payable", 0.0)))
        main_customers = st.text_input("Principais clientes", value=str(company_data.get("main_customers", "")))

    st.subheader("Risco, garantias e qualidade")
    a, b, c = st.columns(3)
    with a:
        guarantee_type = st.text_input("Tipo de garantia", value=str(company_data.get("guarantee_type", "")))
        guarantee_market_value = st.number_input("Valor de mercado da garantia", min_value=0.0, value=float(company_data.get("guarantee_market_value", 0.0)))
        guarantee_liquidation_value = st.number_input("Valor de liquidação da garantia", min_value=0.0, value=float(company_data.get("guarantee_liquidation_value", 0.0)))
        guarantee_encumbrance = st.selectbox("Ónus da garantia", ["nenhum", "incerto", "onus desconhecido"], index=["nenhum", "incerto", "onus desconhecido"].index(str(company_data.get("guarantee_encumbrance", "nenhum")).lower()))
    with b:
        top_customer_concentration = st.number_input("Concentração do maior cliente (%)", min_value=0.0, max_value=100.0, value=float(company_data.get("top_customer_concentration", 0.0)))
        payment_history = st.number_input("Histórico de pagamentos (%)", min_value=0.0, max_value=100.0, value=float(company_data.get("payment_history", 0.0)))
        sector_risk = st.number_input("Risco sectorial (%)", min_value=0.0, max_value=100.0, value=float(company_data.get("sector_risk", 0.0)))
    with c:
        management_quality = st.number_input("Qualidade de gestão (%)", min_value=0.0, max_value=100.0, value=float(company_data.get("management_quality", 0.0)))
        information_quality = st.number_input("Qualidade da informação (%)", min_value=0.0, max_value=100.0, value=float(company_data.get("information_quality", 0.0)))
        compliance_status = st.selectbox("Compliance", ["bom", "atencao", "risco", "critico"], index=["bom", "atencao", "risco", "critico"].index(str(company_data.get("compliance_status", "bom")).lower()))
        documents_complete = st.checkbox("Documentação completa", value=bool(company_data.get("documents_complete", True)))

    submitted = st.form_submit_button("Guardar e validar pedido", type="primary", use_container_width=True)

if submitted:
    payload = {
        **company_data,
        "company_name": company_name, "nif": nif, "sector": sector, "province": province,
        "incorporation_date": incorporation_date, "purpose": purpose, "currency": currency,
        "requested_amount": requested_amount, "requested_term_months": int(requested_term_months),
        "interest_rate": interest_rate, "annual_revenue": annual_revenue, "ebitda": ebitda,
        "net_income": net_income, "total_assets": total_assets, "current_assets": current_assets,
        "cash": cash, "accounts_receivable": accounts_receivable, "total_liabilities": total_liabilities,
        "current_liabilities": current_liabilities, "equity": equity, "existing_debt": existing_debt,
        "annual_interest_expense": annual_interest_expense, "annual_debt_service": annual_debt_service,
        "operating_cash_flow": operating_cash_flow, "capex": capex, "inventory": inventory,
        "accounts_payable": accounts_payable, "main_customers": main_customers,
        "guarantee_type": guarantee_type, "guarantee_market_value": guarantee_market_value,
        "guarantee_liquidation_value": guarantee_liquidation_value, "guarantee_encumbrance": guarantee_encumbrance,
        "top_customer_concentration": top_customer_concentration, "payment_history": payment_history,
        "sector_risk": sector_risk, "management_quality": management_quality,
        "information_quality": information_quality, "compliance_status": compliance_status,
        "documents_complete": documents_complete,
    }
    try:
        CreditApplication.from_dict(payload)
        st.session_state.company_data = payload
        save_company(payload)
        save_application(payload)
        save_audit_event("SUBMIT_APPLICATION", "Analista", str(payload.get("company_id", "")), {"requested_amount": payload.get("requested_amount"), "currency": payload.get("currency")})
        st.success("Pedido validado e guardado na sessão. Consulte as páginas 2 e 3 para a análise.")
    except (TypeError, ValueError) as exc:
        st.error(f"Dados inválidos: {exc}")

st.caption(f"Motor activo: {APP_TITLE}")
