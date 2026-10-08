"""Utilitários reutilizáveis para interface e UX do motor de crédito."""

from __future__ import annotations

import streamlit as st


def apply_global_theme() -> None:
    """Aplica uma identidade visual consistente a todas as páginas."""
    st.markdown(
        """
        <style>
        :root {
            --bg-soft: #f8fafc;
            --bg-strong: #eef4fb;
            --panel: #ffffff;
            --panel-alt: #f8fafc;
            --ink: #0f172a;
            --muted: #475569;
            --primary: #1d4ed8;
            --primary-dark: #0f172a;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --border: #dfe7f2;
            --shadow: rgba(15, 23, 42, 0.08);
        }
        .stApp {
            background: linear-gradient(180deg, var(--bg-soft) 0%, var(--bg-strong) 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1440px;
        }
        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: -0.025em;
        }
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 0.9rem 1rem;
            box-shadow: 0 4px 14px var(--shadow);
        }
        div[data-testid="stMetricLabel"] {
            color: var(--muted);
        }
        .stButton > button, .stFormSubmitButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: transform 120ms ease, box-shadow 120ms ease;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px var(--shadow);
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }
        .kpi-card,
        .panel-card,
        .status-pill,
        .decision-banner,
        .monitor-box {
            border-radius: 16px;
            box-shadow: 0 8px 20px var(--shadow);
        }
        .kpi-card {
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
            color: white;
            padding: 1.1rem 1rem;
            border: 1px solid rgba(148, 163, 184, 0.20);
        }
        .kpi-label { color: #cbd5e1; font-size: 0.75rem; letter-spacing: 0.04em; margin-bottom: 0.3rem; }
        .kpi-value { font-size: 1.7rem; font-weight: 700; }
        .panel-card {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid var(--border);
            padding: 1rem 1.1rem;
        }
        .section-panel {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
        }
        .recommendation-box {
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
            border-radius: 18px;
            padding: 1.2rem 1.4rem;
            border: 1px solid rgba(96, 165, 250, 0.35);
            color: white;
            box-shadow: 0 8px 20px rgba(29, 78, 216, 0.25);
        }
        .decision-banner {
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
            color: white;
            padding: 1.3rem 1.4rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(96, 165, 250, 0.35);
        }
        .status-pill {
            display: inline-block;
            padding: 0.42rem 0.7rem;
            font-weight: 600;
            font-size: 0.78rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            background: #e2e8f0;
            color: var(--ink);
        }
        .status-good {
            background: rgba(16, 185, 129, 0.10);
            border-left: 4px solid var(--success);
            padding: 0.7rem 0.8rem;
            border-radius: 10px;
        }
        .status-warning {
            background: rgba(245, 158, 11, 0.12);
            border-left: 4px solid var(--warning);
            padding: 0.7rem 0.8rem;
            border-radius: 10px;
        }
        .status-danger {
            background: rgba(239, 68, 68, 0.12);
            border-left: 4px solid var(--danger);
            padding: 0.7rem 0.8rem;
            border-radius: 10px;
        }
        .monitor-box {
            background: white;
            border: 1px solid var(--border);
            padding: 1rem;
        }
        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--primary-dark) 0%, #111827 100%);
        }
        div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        div[data-testid="stSidebar"] label {
            color: #e2e8f0;
        }
        [data-testid="stSidebarNav"] {
            background: transparent;
        }
        .stTabs [role="tablist"] {
            gap: 0.5rem;
        }
        .stTabs [role="tab"] {
            border-radius: 10px 10px 0 0;
            padding: 0.55rem 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def safe_float(value: object, default: float = 0.0) -> float:
    """Converte valores de input para float sem falhar em valores vazios."""
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def format_currency(value: float | int, currency: str = "Kz") -> str:
    """Formata montantes em estilo financeiro de demonstração."""
    return f"{currency} {float(value):,.0f}"
