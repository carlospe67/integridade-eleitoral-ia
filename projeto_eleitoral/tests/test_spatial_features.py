from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from synthetic_pipeline import generate_synthetic_data
from spatial_features import calculate_spatial_indicators, compute_lisa


def test_calculate_spatial_indicators() -> None:
    data = generate_synthetic_data(n_sections=50)
    res = calculate_spatial_indicators(data)
    assert "share_candidate" in res.columns
    assert "turnout_rate" in res.columns


def test_compute_lisa() -> None:
    data = generate_synthetic_data(n_sections=50)
    res = compute_lisa(data, feature_col="share_candidate", k=4)
    assert "lisa_iv" in res.columns
    assert "lisa_p_value" in res.columns
    assert "lisa_quadrant_label" in res.columns
    assert len(res) == 50
