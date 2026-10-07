from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from synthetic_pipeline import detect_anomalies, generate_synthetic_data


def test_synthetic_data_has_controlled_patterns() -> None:
    data = generate_synthetic_data(n_sections=100)

    assert len(data) == 100
    assert set(data["synthetic_pattern"]) == {
        "normal",
        "coercion_compatible",
        "purchase_compatible",
    }


def test_detector_flags_controlled_patterns() -> None:
    result = detect_anomalies(generate_synthetic_data(n_sections=100))
    flagged = result.loc[result["anomaly_label"] == -1]

    assert len(flagged) >= 5
    assert flagged["synthetic_pattern"].isin(
        {"coercion_compatible", "purchase_compatible"}
    ).mean() >= 0.5
    assert isinstance(result, pd.DataFrame)
