"""Experimento inicial com dados eleitorais sintéticos e Isolation Forest."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "share_candidate",
    "turnout_rate",
    "delta_historico",
    "concentration_index",
]


def generate_synthetic_data(
    n_sections: int = 200,
    random_state: int = 42,
) -> pd.DataFrame:
    """Generate reproducible section-level data for a controlled experiment."""
    if n_sections < 20:
        raise ValueError("n_sections must be at least 20")

    rng = np.random.default_rng(random_state)
    data = pd.DataFrame(
        {
            "section_id": [f"S{index:04d}" for index in range(n_sections)],
            "x": rng.uniform(-43.8, -43.1, n_sections),
            "y": rng.uniform(-23.1, -22.7, n_sections),
            "share_candidate": np.clip(rng.normal(0.42, 0.08, n_sections), 0.05, 0.95),
            "turnout_rate": np.clip(rng.normal(0.78, 0.06, n_sections), 0.4, 0.98),
            "delta_historico": rng.normal(0.02, 0.08, n_sections),
            "concentration_index": np.clip(rng.normal(0.28, 0.08, n_sections), 0.02, 0.9),
            "synthetic_pattern": "normal",
        }
    )

    coercion_indices = np.arange(min(5, n_sections))
    data.loc[coercion_indices, "share_candidate"] = rng.uniform(0.86, 0.96, len(coercion_indices))
    data.loc[coercion_indices, "concentration_index"] = rng.uniform(0.82, 0.98, len(coercion_indices))
    data.loc[coercion_indices, "synthetic_pattern"] = "coercion_compatible"

    purchase_indices = np.arange(min(5, n_sections), min(10, n_sections))
    data.loc[purchase_indices, "turnout_rate"] = rng.uniform(0.95, 0.99, len(purchase_indices))
    data.loc[purchase_indices, "delta_historico"] = rng.uniform(0.35, 0.65, len(purchase_indices))
    data.loc[purchase_indices, "synthetic_pattern"] = "purchase_compatible"
    return data


def detect_anomalies(data: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """Score rows with Isolation Forest using only documented numeric features."""
    missing_columns = sorted(set(FEATURE_COLUMNS) - set(data.columns))
    if missing_columns:
        raise ValueError(f"Missing feature columns: {', '.join(missing_columns)}")

    result = data.copy()
    scaler = StandardScaler()
    features = scaler.fit_transform(result[FEATURE_COLUMNS])
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=200,
    )
    result["anomaly_label"] = model.fit_predict(features)
    result["anomaly_score"] = -model.score_samples(features)
    return result.sort_values("anomaly_score", ascending=False).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    project_root = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "outputs" / "synthetic_anomalies.csv",
    )
    args = parser.parse_args()

    detected = detect_anomalies(generate_synthetic_data())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    detected.to_csv(args.output, index=False)
    print(f"Saved {len(detected)} rows to {args.output}")
    print(detected[["section_id", "synthetic_pattern", "anomaly_label", "anomaly_score"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
