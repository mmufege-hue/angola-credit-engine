"""Página de score e decisão."""

from __future__ import annotations

import streamlit as st

from analysis_engine import analyse_credit
from database import save_analysis, save_audit_event
from sample_data import load_demo_companies
from ui_helpers import apply_global_theme

apply_global_theme()

st.title("3. Score e Decisão")
company = st.session_state.get("company_data", load_demo_companies()[0].copy())

analysis = analyse_credit(company)
metrics = analysis["metrics"]
score = analysis["score"]
final_class = analysis["risk_class"]
block_rules = analysis["blocking"]
recommendation = analysis["recommendation"]

st.markdown(f"<div class='decision-banner'><strong>RECOMENDAÇÃO:</strong> {recommendation['recommendation']}<br><span>Score final: {score:.2f}/100 · Classe {final_class}</span></div>", unsafe_allow_html=True)

metric_cols = st.columns(2)
with metric_cols[0]:
    st.metric("Score final", f"{score:.2f}/100", help="Score explicável, ponderado pelas regras do modelo.")
with metric_cols[1]:
    st.metric("Classificação", final_class, help="Classe de risco final do pedido.")

if recommendation["recommendation"] in {"Aprovar", "Aprovar com condições"}:
    st.success("Pedido dentro dos critérios de risco toleráveis para esta demonstração.")
elif recommendation["recommendation"] == "Decisão bloqueada":
    st.warning("A decisão foi bloqueada por regras de controlo do protótipo.")
else:
    st.info("A recomendação exige mitigação, reforço documental ou reestruturação.")

if st.button("Registar esta análise no histórico", type="primary"):
    save_analysis({
        "company_id": company.get("company_id", ""),
        "user_name": st.session_state.get("profile", "Analista"),
        "score": score,
        "risk_class": final_class,
        "recommendation": recommendation["recommendation"],
        "explanation": "; ".join(recommendation["negative_factors"]),
        "conditions": recommendation["conditions"],
    })
    save_audit_event("REGISTER_ANALYSIS", st.session_state.get("profile", "Analista"), str(company.get("company_id", "")), {"score": score, "risk_class": final_class, "recommendation": recommendation["recommendation"]})
    st.success("Análise registada no histórico de auditoria.")

if block_rules["block_decision"]:
    st.markdown("<div class='status-danger'><strong>Decisão bloqueada por regras de controlo.</strong></div>", unsafe_allow_html=True)
    for reason in block_rules["reasons"]:
        st.write(f"- {reason}")

st.subheader("Factores positivos")
for item in recommendation["positive_factors"]:
    st.markdown(f"<div class='status-good'>• {item}</div>", unsafe_allow_html=True)

st.subheader("Factores negativos")
for item in recommendation["negative_factors"]:
    st.markdown(f"<div class='status-warning'>• {item}</div>", unsafe_allow_html=True)

st.subheader("Alertas críticos")
if recommendation["alerts"]:
    for item in recommendation["alerts"]:
        st.markdown(f"<div class='status-danger'>• {item}</div>", unsafe_allow_html=True)
else:
    st.info("Sem alertas críticos relevantes para esta análise.")

st.subheader("Condições sugeridas")
for item in recommendation["conditions"]:
    st.write(f"- {item}")

st.subheader("Dados em falta")
if recommendation["missing_data"]:
    for item in recommendation["missing_data"]:
        st.write(f"- {item}")
else:
    st.write("Nenhum dado essencial em falta.")

st.subheader("Limitações do modelo")
st.write("Este protótipo é baseado em regras transparentes, dados fictícios e não substitui a análise do comité de crédito ou a validação regulatória da instituição.")
