"""Página de análise financeira."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from analysis_engine import credit_metrics
from calculations import (
    calculate_current_ratio,
    calculate_dscr,
    calculate_ebitda_margin,
    calculate_guarantee_coverage,
    calculate_interest_coverage,
    calculate_ltv,
    calculate_net_margin,
    calculate_quick_ratio,
    calculate_receivable_days,
)
from sample_data import load_demo_companies
from ui_helpers import apply_global_theme

st.markdown(
    """
    <style>
    .stApp { background: #f8fafc; }
    .section-card { background: white; border-radius: 14px; border: 1px solid #e2e8f0; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05); }
    .kpi-dark { background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%); color: white; border-radius: 14px; padding: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)
apply_global_theme()

st.title("2. Análise Financeira")
company = st.session_state.get("company_data", load_demo_companies()[0])

if not company:
    st.warning("Nenhum pedido carregado.")
    st.stop()

revenue = float(company.get("annual_revenue", 0.0))
ebitda = float(company.get("ebitda", 0.0))
net_income = float(company.get("net_income", 0.0))
requested_amount = float(company.get("requested_amount", 0.0))
liquidation = float(company.get("guarantee_liquidation_value", 0.0))
receivables = float(company.get("accounts_receivable", 0.0))
core = credit_metrics(company)
metrics = {
    "Liquidez corrente": core["current_ratio"],
    "Liquidez imediata": core["quick_ratio"],
    "Margem EBITDA": ebitda / revenue if revenue else 0.0,
    "Margem líquida": net_income / revenue if revenue else 0.0,
    "Dívida/EBITDA": core["debt_to_ebitda"],
    "Cobertura de juros": core["interest_coverage"],
    "DSCR": core["dscr"],
    "Prazo médio de recebimento (dias)": (receivables / revenue * 365.0) if revenue else 0.0,
    "LTV": requested_amount / liquidation if liquidation else 0.0,
    "Cobertura da garantia": core["guarantee_coverage"],
}

col1, col2, col3, col4 = st.columns(4)
for metric_name, metric_value in list(metrics.items())[:4]:
    col = col1 if metric_name == "Liquidez corrente" else col2 if metric_name == "Liquidez imediata" else col3 if metric_name == "Margem EBITDA" else col4
    with col:
        st.markdown(f"<div class='kpi-dark'><strong>{metric_name}</strong><br>{metric_value:.2f}</div>", unsafe_allow_html=True)

st.markdown("---")

financial_df = pd.DataFrame(
    {"Indicador": list(metrics.keys()), "Valor": list(metrics.values())}
)
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.dataframe(financial_df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

fig = px.bar(
    financial_df,
    x="Indicador",
    y="Valor",
    color="Indicador",
    title="Indicadores financeiros principais",
    color_discrete_sequence=["#0f172a", "#1d4ed8", "#10b981", "#f59e0b", "#64748b", "#cbd5e1", "#ef4444", "#94a3b8", "#0ea5e9", "#14b8a6"],
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Interpretação")
for name, value in metrics.items():
    if name == "Liquidez corrente":
        interpretation = "Bom" if value >= 1.5 else "Aceitável" if value >= 1.0 else "Fraco"
    elif name == "DSCR":
        interpretation = "Sólido" if value >= 1.5 else "Aceitável" if value >= 1.0 else "Crítico"
    elif name == "Dívida/EBITDA":
        interpretation = "Baixo risco" if value <= 2.0 else "Moderado" if value <= 3.5 else "Elevado"
    else:
        interpretation = "Sem alerta"
    st.write(f"- {name}: {value:.2f} — {interpretation}.")

st.info("Aviso: quando um dado não estiver disponível, a estimativa é identificada e a métrica pode ser tratada como aproximada.")
