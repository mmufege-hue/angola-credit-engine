"""Página do módulo opcional de machine learning."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ml_model import (
    MODEL_WARNING,
    build_company_features,
    build_synthetic_dataset,
    low_reliability_warning,
    save_model_metadata,
    select_best_model,
    train_and_compare_models,
)
from sample_data import load_demo_companies
from ui_helpers import apply_global_theme


@st.cache_resource(show_spinner="A treinar modelos com dados sintéticos...")
def load_experimental_models():
    dataset = build_synthetic_dataset(n_rows=320, random_state=42)
    results = train_and_compare_models(dataset)
    saved_metadata = save_model_metadata(results)
    return results, saved_metadata


st.markdown(
    """
    <style>
    .stApp { background: #f8fafc; }
    .experimental-banner {
        background: linear-gradient(135deg, #111827 0%, #1d4ed8 100%);
        border-radius: 18px;
        color: white;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 20px rgba(29, 78, 216, 0.16);
    }
    .panel {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
apply_global_theme()

st.title("8. Modelo Experimental")
st.caption("Este módulo é opcional e não substitui o motor baseado em regras.")

company = st.session_state.get("company_data", load_demo_companies()[0])

st.info("Sem aprovação automática. O score baseado em regras continua a ser a decisão principal até existir validação adequada.")
st.warning(MODEL_WARNING)
st.caption("Demonstração treinada com 320 registos inteiramente sintéticos. O alvo é um perfil de crédito favorável sintético, não incumprimento observado nem histórico bancário real.")

model_results, metadata = load_experimental_models()

reliability_message = low_reliability_warning(model_results)
if "Baixa fiabilidade" in reliability_message:
    st.warning(reliability_message)
else:
    st.success(reliability_message)

best_name, best_result = select_best_model(model_results)
company_features = build_company_features(company)
probability = float(best_result["model"].predict_proba(company_features)[0, 1])

st.markdown(
    f"""
    <div class='experimental-banner'>
      <strong>Modelo seleccionado:</strong> {best_name.replace('_', ' ').title()}<br>
            <strong>Probabilidade estimada de perfil favorável (rótulo sintético):</strong> {probability:.2%}<br>
            <strong>{MODEL_WARNING}</strong>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Métricas de desempenho")
model_table = []
for name, result in model_results.items():
    metrics = result["metrics"]
    model_table.append(
        {
            "Modelo": name.replace("_", " ").title(),
            "ROC-AUC": round(metrics["roc_auc"], 4),
            "Precisão": round(metrics["precision"], 4),
            "Recall": round(metrics["recall"], 4),
            "F1": round(metrics["f1"], 4),
            "Log Loss": round(metrics["log_loss"], 4),
            "Brier Score": round(metrics["brier_score"], 4),
        }
    )

st.dataframe(pd.DataFrame(model_table), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Matriz de confusão")
    cm = model_results[best_name]["confusion_matrix"]
    st.write(pd.DataFrame(
        cm,
        index=["Real: não favorável", "Real: favorável"],
        columns=["Previsto: não favorável", "Previsto: favorável"],
    ))

with right:
    st.subheader("Importância das variáveis")
    importance = pd.DataFrame(model_results[best_name]["feature_importance"])
    st.bar_chart(importance.set_index("feature")["importance"])

st.subheader("Calibração das probabilidades")
calibration = model_results[best_name]["calibration"]
calibration_chart = go.Figure()
calibration_chart.add_trace(go.Scatter(
    x=calibration["mean_predicted"],
    y=calibration["fraction_positive"],
    mode="lines+markers",
    name="Calibração observada",
))
calibration_chart.add_trace(go.Scatter(
    x=[0, 1], y=[0, 1], mode="lines", name="Calibração ideal",
    line={"dash": "dash", "color": "#64748b"},
))
calibration_chart.update_layout(
    xaxis_title="Probabilidade média prevista",
    yaxis_title="Frequência positiva observada",
    xaxis={"range": [0, 1]},
    yaxis={"range": [0, 1]},
    height=360,
)
st.plotly_chart(calibration_chart, use_container_width=True)
st.caption(f"MAE de calibração: {calibration['mae']:.4f}")

st.subheader("Explicação da decisão")
st.caption("A decisão primária continua a ser o score baseado em regras, com factores, alertas e condições na página Score e Decisão. A importância abaixo descreve o modelo global e não é uma explicação causal individual.")
feature_contribution = model_results[best_name]["feature_importance"]
importance_table = pd.DataFrame(feature_contribution)
importance_table["magnitude"] = importance_table["importance"].abs()
st.dataframe(importance_table.sort_values("magnitude", ascending=False).head(5), use_container_width=True, hide_index=True)
with st.expander("Valores financeiros usados para esta estimativa"):
    st.dataframe(company_features.T.rename(columns={0: "Valor"}), use_container_width=True)

st.subheader("Metadados do modelo")
st.json({
    "versao": metadata["model_version"],
    "data_treino": metadata["trained_at_utc"],
    "variaveis": metadata["feature_columns"],
    "melhor_modelo": metadata["best_model"],
    "tipo_dados": metadata["training_data_type"],
    "amostra_treino_teste": metadata["training_sample_count"],
    "metricas": metadata["metrics"],
    "local_metadados": metadata["metadata_storage_path"],
})

st.caption("A interpretação do modelo é complementar e não substitui o processo de decisão baseado em regras, a validação do risco e a aprovação do comité de crédito.")
