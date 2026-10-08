"""Página de monitorização pós-concessão."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ui_helpers import apply_global_theme

apply_global_theme()

st.title("5. Monitorização")

monitoring = [
    {"Data": "2026-10-01", "DSCR": 1.42, "Receita_3m": 680000, "Entradas_bancarias": 650000, "Dívida_actual": 950000, "Atraso_dias": 12, "Covenant": "Cumprido", "Garantia": 890000, "Compliance": "Normal", "Nível": "Amarelo"},
    {"Data": "2026-09-01", "DSCR": 1.55, "Receita_3m": 720000, "Entradas_bancarias": 700000, "Dívida_actual": 930000, "Atraso_dias": 0, "Covenant": "Cumprido", "Garantia": 920000, "Compliance": "Normal", "Nível": "Verde"},
]

monitoring_df = pd.DataFrame(monitoring)
levels = ["Todos", "Verde", "Amarelo", "Vermelho"]
selected_level = st.selectbox("Filtrar por nível", levels, index=0)
filtered_monitoring = monitoring_df if selected_level == "Todos" else monitoring_df[monitoring_df["Nível"] == selected_level]

st.markdown("<div class='monitor-box'>", unsafe_allow_html=True)
st.dataframe(filtered_monitoring, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.subheader("Alertas")
for row in filtered_monitoring.to_dict("records"):
    if row["Nível"] == "Vermelho":
        st.error(f"{row['Data']}: intervenção requerida")
    elif row["Nível"] == "Amarelo":
        st.warning(f"{row['Data']}: atenção e monitorização reforçada")
    else:
        st.success(f"{row['Data']}: operação em conformidade")
