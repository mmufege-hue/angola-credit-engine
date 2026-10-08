"""Dashboard executivo do portfólio fictício."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from analysis_engine import analyse_credit
from sample_data import load_demo_companies
from ui_helpers import apply_global_theme, format_currency

apply_global_theme()

st.title("6. Dashboard")
st.caption("Visão executiva do portfólio, com indicadores e filtros interactivos.")
companies = load_demo_companies()
rows = []
for company in companies:
    analysis = analyse_credit(company)
    rows.append({
        **company,
        "risk_class": analysis["risk_class"],
        "score": analysis["score"],
        "recommendation": analysis["recommendation"]["recommendation"],
        "ecl_proxy": analysis["ecl_proxy"],
        "dscr": analysis["metrics"]["dscr"],
    })
portfolio_df = pd.DataFrame(rows)

company_options = sorted(portfolio_df["company_name"].dropna().unique().tolist())
sector_options = sorted(portfolio_df["sector"].dropna().unique().tolist())
province_options = sorted(portfolio_df["province"].dropna().unique().tolist())
risk_options = sorted(portfolio_df["risk_class"].dropna().unique().tolist())
decision_options = sorted(portfolio_df["recommendation"].dropna().unique().tolist())

with st.expander("Filtrar portfólio", expanded=True):
    filter_cols = st.columns(3)
    with filter_cols[0]:
        selected_companies = st.multiselect(
            "Empresa",
            options=company_options,
            default=company_options,
            help="Seleccione uma ou mais empresas para limitar os indicadores e gráficos.",
        )
        selected_sectors = st.multiselect("Sector", options=sector_options, default=sector_options)
    with filter_cols[1]:
        selected_provinces = st.multiselect("Província", options=province_options, default=province_options)
        selected_risks = st.multiselect("Classe de risco", options=risk_options, default=risk_options)
    with filter_cols[2]:
        selected_decisions = st.multiselect("Decisão", options=decision_options, default=decision_options)
        st.caption("Os filtros são combinados; todos os indicadores abaixo reflectem apenas os resultados seleccionados.")

filtered_df = portfolio_df[
    portfolio_df["company_name"].isin(selected_companies)
    & portfolio_df["sector"].isin(selected_sectors)
    & portfolio_df["province"].isin(selected_provinces)
    & portfolio_df["risk_class"].isin(selected_risks)
    & portfolio_df["recommendation"].isin(selected_decisions)
].copy()

if filtered_df.empty:
    st.warning("Nenhuma empresa corresponde aos filtros aplicados. Ajuste os critérios para rever o portfólio.")
    st.stop()

st.caption(f"A mostrar {len(filtered_df)} de {len(portfolio_df)} empresas.")
approved_mask = filtered_df["recommendation"].isin(["Aprovar", "Aprovar com condições"])
requested_total = filtered_df["requested_amount"].sum()
approved_total = filtered_df.loc[approved_mask, "requested_amount"].sum()
ecl_total = filtered_df["ecl_proxy"].sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de pedidos", f"{len(filtered_df)}")
with col2:
    st.metric("Montante solicitado", format_currency(requested_total))
with col3:
    st.metric("Montante aprovável", format_currency(approved_total))
with col4:
    st.metric("ECL proxy", format_currency(ecl_total), help="PD x LGD proxy x EAD. Não é ECL IFRS 9 validada.")

st.caption("Todos os valores são fictícios. A ECL apresentada é uma aproximação pedagógica e não substitui um modelo IFRS 9 validado.")
st.markdown("---")

left, right = st.columns(2)
with left:
    pie_fig = px.pie(
        filtered_df,
        names="sector",
        values="requested_amount",
        title="Exposição por sector",
        hole=0.48,
        color_discrete_sequence=["#1d4ed8", "#10b981", "#f59e0b", "#64748b"],
    )
    pie_fig.update_traces(textposition="inside", textinfo="percent+label", hovertemplate="%{label}<br>Kz %{value:,.0f}<extra></extra>")
    pie_fig.update_layout(template="plotly_white", margin=dict(l=12, r=12, t=58, b=12), legend_title_text="Sector")
    st.plotly_chart(pie_fig, use_container_width=True)
with right:
    bar_fig = px.bar(
        filtered_df.sort_values(["score", "company_name"], ascending=[True, True]),
        x="score",
        y="company_name",
        color="risk_class",
        orientation="h",
        title="Score de risco por empresa",
        labels={"score": "Score / 100", "company_name": "Empresa", "risk_class": "Classe"},
        color_discrete_map={"A": "#10b981", "B": "#3b82f6", "C": "#f59e0b", "D": "#f97316", "E": "#ef4444"},
        hover_data={"recommendation": True, "dscr": ":.2f", "score": ":.1f"},
    )
    bar_fig.update_layout(template="plotly_white", margin=dict(l=12, r=12, t=58, b=12), xaxis_range=[0, 100])
    bar_fig.update_xaxes(title="Score / 100")
    st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("---")
st.subheader("Resumo de risco")
st.dataframe(
    filtered_df[["company_name", "sector", "province", "requested_amount", "dscr", "score", "risk_class", "recommendation", "ecl_proxy"]].rename(columns={
        "company_name": "Empresa", "sector": "Sector", "province": "Província", "requested_amount": "Montante", "dscr": "DSCR", "score": "Score", "risk_class": "Classe", "recommendation": "Decisão", "ecl_proxy": "ECL proxy"
    }),
    use_container_width=True,
    hide_index=True,
)
