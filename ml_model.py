"""Módulo opcional de machine learning para apoio experimental à decisão de crédito.

Este módulo não substitui o score baseado em regras. O modelo é treinado apenas com
variáveis financeiras e operacionais fictícias, sem uso de dados protegidos.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    brier_score_loss,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

MODEL_VERSION = "0.1.0"
MODEL_WARNING = "Probabilidade estimada pelo modelo experimental — não validada para decisões reais."
MIN_RELIABLE_SAMPLE_SIZE = 500

FEATURE_COLUMNS = [
    "dscr",
    "current_ratio",
    "debt_to_ebitda",
    "payment_history",
    "top_customer_concentration",
    "guarantee_coverage",
    "management_quality",
    "information_quality",
]


def build_synthetic_dataset(n_rows: int = 500, random_state: int = 42) -> pd.DataFrame:
    """Cria um conjunto sintético de empresas fictícias sem dados protegidos."""
    rng = np.random.default_rng(random_state)

    df = pd.DataFrame(
        {
            "dscr": rng.uniform(0.6, 2.9, size=n_rows),
            "current_ratio": rng.uniform(0.5, 2.8, size=n_rows),
            "debt_to_ebitda": rng.uniform(0.4, 7.0, size=n_rows),
            "payment_history": rng.uniform(25, 98, size=n_rows),
            "top_customer_concentration": rng.uniform(5, 75, size=n_rows),
            "guarantee_coverage": rng.uniform(0.2, 1.6, size=n_rows),
            "management_quality": rng.uniform(35, 95, size=n_rows),
            "information_quality": rng.uniform(40, 98, size=n_rows),
        }
    )

    favorable_profile_signal = (
        0.75 * (df["dscr"] - 1.2)
        + 0.35 * (df["current_ratio"] - 1.1)
        - 0.28 * (df["debt_to_ebitda"] - 3.0)
        + 0.015 * (df["payment_history"] - 70)
        - 0.012 * (df["top_customer_concentration"] - 35)
        + 0.20 * (df["guarantee_coverage"] - 0.8)
        + 0.008 * (df["management_quality"] - 65)
        + 0.006 * (df["information_quality"] - 70)
        + rng.normal(0, 0.6, size=n_rows)
    )
    df["target"] = (favorable_profile_signal >= 0).astype(int)
    df["target"] = np.where(rng.random(n_rows) < 0.03, 1 - df["target"], df["target"])
    df["target"] = df["target"].clip(0, 1).astype(int)
    return df


def _safe_metrics(y_true: np.ndarray, y_pred: np.ndarray, probabilities: np.ndarray) -> dict[str, float]:
    return {
        "roc_auc": float(roc_auc_score(y_true, probabilities)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "log_loss": float(log_loss(y_true, probabilities, labels=[0, 1])),
        "brier_score": float(brier_score_loss(y_true, probabilities)),
    }


def _calibration_summary(y_true: np.ndarray, probabilities: np.ndarray, n_bins: int = 10) -> dict[str, Any]:
    bins = np.linspace(0, 1, n_bins + 1)
    mean_pred, fraction_pos = calibration_curve(y_true, probabilities, n_bins=n_bins, strategy="uniform")
    calibration = {
        "bins": [float(value) for value in bins],
        "mean_predicted": [float(value) for value in mean_pred.tolist()],
        "fraction_positive": [float(value) for value in fraction_pos.tolist()],
        "mae": float(np.mean(np.abs(mean_pred - fraction_pos))),
    }
    return calibration


def _feature_importance(model: Any, feature_names: list[str]) -> list[dict[str, Any]]:
    estimator = model.steps[-1][1] if hasattr(model, "steps") else model
    if hasattr(estimator, "coef_"):
        values = np.ravel(estimator.coef_)
        feature_values = {name: float(value) for name, value in zip(feature_names, values)}
    elif hasattr(estimator, "feature_importances_"):
        values = np.ravel(estimator.feature_importances_)
        feature_values = {name: float(value) for name, value in zip(feature_names, values)}
    else:
        feature_values = {name: 0.0 for name in feature_names}

    ordered = sorted(feature_values.items(), key=lambda item: abs(item[1]), reverse=True)
    return [{"feature": name, "importance": float(value)} for name, value in ordered]


def _evaluate_model(model: Any, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series) -> dict[str, Any]:
    _ = X_train, y_train
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    metrics = _safe_metrics(y_test.to_numpy(), predictions, probabilities)
    confusion = confusion_matrix(y_test, predictions).tolist()
    calibration = _calibration_summary(y_test.to_numpy(), probabilities)

    return {
        "model": model,
        "metrics": metrics,
        "confusion_matrix": confusion,
        "feature_importance": _feature_importance(model, list(X_test.columns)),
        "calibration": calibration,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "n_samples": int(len(X_train) + len(X_test)),
    }


def train_and_compare_models(dataframe: pd.DataFrame) -> dict[str, dict[str, Any]]:
    """Treina e compara Logistic Regression versus Random Forest."""
    X = dataframe[FEATURE_COLUMNS]
    y = dataframe["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    logistic_model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, random_state=42),
    )
    random_forest_model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        min_samples_leaf=2,
    )

    logistic_model.fit(X_train, y_train)
    random_forest_model.fit(X_train, y_train)

    return {
        "logistic_regression": _evaluate_model(logistic_model, X_train, X_test, y_train, y_test),
        "random_forest": _evaluate_model(random_forest_model, X_train, X_test, y_train, y_test),
    }


def select_best_model(model_results: dict[str, dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    """Escolhe o melhor modelo pela maior ROC-AUC."""
    best_name, best_result = max(
        model_results.items(),
        key=lambda item: item[1]["metrics"]["roc_auc"],
    )
    return best_name, best_result


def build_company_features(company_data: dict[str, Any]) -> pd.DataFrame:
    """Converte os dados de uma empresa para um DataFrame usado pela previsão experimental."""
    requested_amount = float(company_data.get("requested_amount", 0.0))
    liquidation = float(company_data.get("guarantee_liquidation_value", 0.0))
    current_assets = float(company_data.get("current_assets", 0.0)) or float(company_data.get("total_assets", 0.0) * 0.4)
    current_liabilities = float(company_data.get("current_liabilities", 0.0)) or float(company_data.get("total_liabilities", 0.0) * 0.3)
    operating_cash_flow = float(company_data.get("operating_cash_flow", 0.0))
    annual_debt_service = float(company_data.get("annual_debt_service", 0.0))
    existing_debt = float(company_data.get("existing_debt", 0.0))
    ebitda = float(company_data.get("ebitda", 0.0))
    q = {
        "dscr": float(operating_cash_flow / annual_debt_service) if annual_debt_service else 0.0,
        "current_ratio": float(current_assets / current_liabilities) if current_liabilities else 0.0,
        "debt_to_ebitda": float(existing_debt / ebitda) if ebitda else 0.0,
        "payment_history": float(company_data.get("payment_history", 0.0)),
        "top_customer_concentration": float(company_data.get("top_customer_concentration", 0.0)),
        "guarantee_coverage": float(liquidation / requested_amount) if requested_amount else 0.0,
        "management_quality": float(company_data.get("management_quality", 0.0)),
        "information_quality": float(company_data.get("information_quality", 0.0)),
    }
    return pd.DataFrame([q], columns=FEATURE_COLUMNS)


def save_model_metadata(model_results: dict[str, dict[str, Any]], output_path: str | None = None) -> dict[str, Any]:
    """Guarda a versão do modelo, metadados, variáveis e métricas."""
    best_name, best_result = select_best_model(model_results)

    payload = {
        "model_version": MODEL_VERSION,
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "best_model": best_name,
        "training_data_type": "synthetic_demo_only",
        "training_sample_count": best_result["n_samples"],
        "target_definition": "perfil_crediticio_favoravel_sintetico; nao representa incumprimento real",
        "feature_columns": FEATURE_COLUMNS,
        "metrics": best_result["metrics"],
        "confusion_matrix": best_result["confusion_matrix"],
        "feature_importance": best_result["feature_importance"],
        "calibration": best_result["calibration"],
        "experimental_warning": MODEL_WARNING,
    }

    path = Path(output_path) if output_path else Path(__file__).resolve().parent / "data" / "ml_model_metadata.json"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except PermissionError:
        local_app_data = Path.home() / "AppData" / "Local" / "AngolaCreditEngine"
        path = local_app_data / "ml_model_metadata.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    payload["metadata_storage_path"] = str(path)
    return payload


def low_reliability_warning(model_results: dict[str, dict[str, Any]]) -> str:
    """Identifica baixa fiabilidade quando o conjunto é pequeno ou instável."""
    sample_count = max((item["n_samples"] for item in model_results.values()), default=0)
    if sample_count < MIN_RELIABLE_SAMPLE_SIZE:
        return "Baixa fiabilidade: conjunto de dados insuficiente para validação robusta. Os resultados são experimentais."
    return "Conjunto de treino e teste suficiente para uma primeira validação experimental."
