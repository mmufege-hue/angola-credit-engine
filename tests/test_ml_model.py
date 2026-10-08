import pandas as pd

from ml_model import (
    build_synthetic_dataset,
    low_reliability_warning,
    save_model_metadata,
    train_and_compare_models,
)


def test_build_synthetic_dataset_has_expected_structure():
    df = build_synthetic_dataset(n_rows=50)
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 50
    assert {"dscr", "current_ratio", "debt_to_ebitda", "payment_history", "top_customer_concentration", "guarantee_coverage", "management_quality", "information_quality", "target"}.issubset(df.columns)
    assert df["target"].isin([0, 1]).all()
    assert df["target"].nunique() == 2


def test_train_and_compare_models_returns_metrics():
    df = build_synthetic_dataset(n_rows=120)
    result = train_and_compare_models(df)

    assert set(result.keys()) == {"logistic_regression", "random_forest"}
    for model_name, model_info in result.items():
        assert "model" in model_info
        assert "metrics" in model_info
        assert model_info["metrics"]["roc_auc"] >= 0.0
        assert model_info["metrics"]["precision"] >= 0.0
        assert model_info["metrics"]["recall"] >= 0.0
        assert model_info["metrics"]["f1"] >= 0.0
        assert model_info["metrics"]["log_loss"] >= 0.0
        assert model_info["metrics"]["brier_score"] >= 0.0
        assert model_info["n_samples"] == 120


def test_small_synthetic_sample_is_marked_low_reliability(tmp_path):
    result = train_and_compare_models(build_synthetic_dataset(n_rows=50))
    assert "Baixa fiabilidade" in low_reliability_warning(result)

    metadata = save_model_metadata(result, str(tmp_path / "model.json"))
    assert metadata["training_data_type"] == "synthetic_demo_only"
    assert metadata["training_sample_count"] == 50
    assert metadata["feature_columns"]
