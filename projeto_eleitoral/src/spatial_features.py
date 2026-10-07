"""Módulo de Engenharia de Atributos Espaciais e Autocorrelação (Moran/LISA)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from esda.moran import Moran_Local
from libpysal.weights import KNN


def calculate_spatial_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores básicos de participação, concentração e variação."""
    result = data.copy()
    if "turnout_rate" not in result.columns and {"voters", "abstentions"}.issubset(result.columns):
        total = result["voters"] + result["abstentions"]
        result["turnout_rate"] = result["voters"] / total.replace(0, np.nan)
    
    if "share_candidate" not in result.columns and {"candidate_votes", "total_valid_votes"}.issubset(result.columns):
        result["share_candidate"] = result["candidate_votes"] / result["total_valid_votes"].replace(0, np.nan)
        
    return result


def compute_lisa(
    data: pd.DataFrame,
    feature_col: str,
    k: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Calcula Moran Local (LISA) usando K-Nearest Neighbors nas coordenadas (x, y)."""
    required = {"section_id", "x", "y", feature_col}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Colunas ausentes para LISA: {missing}")

    df = data.copy().dropna(subset=[feature_col, "x", "y"]).reset_index(drop=True)
    if len(df) < k + 1:
        raise ValueError(f"Número de amostras ({len(df)}) insuficiente para k={k}")

    coords = df[["x", "y"]].values
    w = KNN.from_array(coords, k=k)
    w.transform = "r"  # row-standardized

    y = df[feature_col].values
    lm = Moran_Local(y, w, seed=random_state)

    df["lisa_iv"] = lm.Is
    df["lisa_p_value"] = lm.p_sim
    df["lisa_quadrant"] = lm.q  # 1: HH, 2: LH, 3: LL, 4: HL

    quadrant_labels = {1: "High-High", 2: "Low-High", 3: "Low-Low", 4: "High-Low"}
    df["lisa_quadrant_label"] = df["lisa_quadrant"].map(quadrant_labels)

    return df
