"""Página de stress testing."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from sample_data import load_demo_companies
from stress_testing import run_scenarios
from ui_helpers import apply_global_theme

st.markdown(
    """
    <style>
    .stApp { background: #f8fafc; }
    .pressure-box { background: white; border-radius: 14px; border: 1px solid #e2e8f0; padding: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)
apply_global_theme()

st.title("4. Stress Testing")
company = st.session_state.get("company_data", load_demo_companies()[0])
scenarios = run_scenarios({
    "annual_revenue": float(company.get("annual_revenue", 0.0)),
    "ebitda": float(company.get("ebitda", 0.0)),
    "operating_cash_flow": float(company.get("operating_cash_flow", 0.0)),
    "capex": float(company.get("capex", 0.0)),
    "annual_debt_service": float(company.get("annual_debt_service", 0.0)),
    "current_assets": float(company.get("total_assets", 0.0) * 0.4),
    "current_liabilities": float(company.get("total_liabilities", 0.0) * 0.3),
    "existing_debt": float(company.get("existing_debt", 0.0)),
    "guarantee_liquidation_value": float(company.get("guarantee_liquidation_value", 0.0)),
    "requested_amount": float(company.get("requested_amount", 0.0)),
    "interest_rate": float(company.get("interest_rate", 0.0)),
    "currency": str(company.get("currency", "AOA")).upper(),
    "foreign_currency_debt_percentage": float(company.get("foreign_currency_debt_percentage", 0.0)),
})

scenario_df = pd.DataFrame.from_dict(scenarios, orient="index")
scenario_df = scenario_df.reset_index().rename(columns={"index": "Cenário"})
st.markdown("<div class='pressure-box'>", unsafe_allow_html=True)
st.dataframe(scenario_df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

fig = px.bar(scenario_df, x="Cenário", y="dscr", color="Cenário", title="DSCR por cenário", color_discrete_sequence=["#0f172a", "#f59e0b", "#ef4444"])
st.plotly_chart(fig, use_container_width=True)

st.subheader("Resultado resumido")
for scenario_name, result in scenarios.items():
    st.write(f"- {scenario_name.title()}: DSCR {result['dscr']:.2f}x, decisão {result['decision']}")
