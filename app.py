"""Aplicação principal do motor de decisão de crédito corporativo."""

from __future__ import annotations

import streamlit as st

from config import APP_TITLE, REPORT_WARNING, RULES_VERSION
from analysis_engine import analyse_credit
from sample_data import load_demo_companies
from database import initialize_database
from ui_helpers import apply_global_theme, format_currency


st.set_page_config(page_title=APP_TITLE, page_icon="🏦", layout="wide")
initialize_database()
apply_global_theme()

if "company_data" not in st.session_state:
    st.session_state.company_data = load_demo_companies()[0].copy()

if "profile" not in st.session_state:
    st.session_state.profile = "Analista"

st.title(APP_TITLE)
st.caption(REPORT_WARNING)
st.caption(f"Versão das regras: {RULES_VERSION}")

st.sidebar.title("Navegação")
st.sidebar.write("Perfil de acesso")
profile = st.sidebar.selectbox("Perfil", ["Analista", "Risco", "Administrador"], index=["Analista", "Risco", "Administrador"].index(st.session_state.get("profile", "Analista")), help="Perfil demonstrativo, sem autenticação real.")
st.session_state.profile = profile
st.sidebar.write(f"Perfil activo: {profile}")

st.sidebar.markdown("---")
st.sidebar.warning("Módulo experimental disponível na página de ML. O score baseado em regras continua a ser a decisão principal e não há aprovação automática.")
st.sidebar.info("Não usar dados reais de clientes; este protótipo utiliza apenas empresas fictícias.")

demo_companies = load_demo_companies()
demo_analyses = [analyse_credit(company) for company in demo_companies]
requested_total = sum(float(c.get("requested_amount", 0)) for c in demo_companies)
approved_total = sum(float(c.get("requested_amount", 0)) for c, a in zip(demo_companies, demo_analyses) if a["recommendation"]["recommendation"] in {"Aprovar", "Aprovar com condições"})
ecl_total = sum(a["ecl_proxy"] for a in demo_analyses)
avg_dscr = sum(a["metrics"]["dscr"] for a in demo_analyses) / len(demo_analyses)
kpi_cols = st.columns(4)
with kpi_cols[0]:
    st.markdown('<div class="kpi-card"><div class="kpi-label">Pedidos demonstrativos</div><div class="kpi-value">{}</div></div>'.format(len(demo_companies)), unsafe_allow_html=True)
with kpi_cols[1]:
    st.markdown('<div class="kpi-card"><div class="kpi-label">Montante solicitado</div><div class="kpi-value">{}</div></div>'.format(format_currency(requested_total)), unsafe_allow_html=True)
with kpi_cols[2]:
    st.markdown('<div class="kpi-card"><div class="kpi-label">Montante aprovável</div><div class="kpi-value">{}</div></div>'.format(format_currency(approved_total)), unsafe_allow_html=True)
with kpi_cols[3]:
    st.markdown('<div class="kpi-card"><div class="kpi-label">ECL proxy</div><div class="kpi-value">{}</div></div>'.format(format_currency(ecl_total)), unsafe_allow_html=True)

st.caption(f"DSCR médio demonstrativo: {avg_dscr:.2f}x · ECL proxy = PD × LGD proxy × EAD; não é ECL IFRS 9 validada.")

class_counts = {}
for analysis in demo_analyses:
    risk_class = analysis["risk_class"]
    class_counts[risk_class] = class_counts.get(risk_class, 0) + 1

max_class_count = max(class_counts.values())
dominant_classes = ", ".join(
    risk_class for risk_class, count in sorted(class_counts.items()) if count == max_class_count
)
best_company, best_analysis = max(
    zip(demo_companies, demo_analyses),
    key=lambda item: item[1]["score"],
)

st.markdown("---")

left, right = st.columns([1.4, 1])
with left:
    st.subheader("Resumo executivo")
    st.markdown(
        """
        <div class='section-panel'>
        Este protótipo é uma ferramenta de apoio à decisão, com regras transparentes, observabilidade dos factores e registo de auditoria.
        A decisão não substitui o comité de crédito nem a validação interna da instituição financeira.
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.subheader("Indicadores principais")
    st.metric("DSCR médio", f"{avg_dscr:.2f}x", help="Cobertura anual do serviço da dívida.")
    st.metric("Cliente principal", f"{max(float(c.get('top_customer_concentration', 0)) for c in demo_companies):.0f}%", help="Concentração do principal cliente na carteira analisada.")
    st.metric("Classe(s) mais frequente(s)", dominant_classes, help="Classe(s) com maior número de empresas no portfólio demonstrativo.")

st.markdown("---")

st.subheader("Recomendação de topo")
with st.container(border=True):
    recommendation_cols = st.columns([2, 1, 1])
    with recommendation_cols[0]:
        st.markdown(f"**{best_company['company_name']}**")
        st.caption("Maior score de risco entre as empresas demonstrativas; não constitui aprovação.")
    with recommendation_cols[1]:
        st.metric("Recomendação", best_analysis["recommendation"]["recommendation"])
    with recommendation_cols[2]:
        st.metric("Score / classe", f"{best_analysis['score']:.1f} · {best_analysis['risk_class']}")

st.markdown("---")

st.write("Use o menu lateral para navegar entre o pedido, análise, score, stress testing, monitorização, dashboard e auditoria.")
