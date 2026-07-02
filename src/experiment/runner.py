"""Lógica interna del proceso experimental.

Este módulo no se documenta ni se expone al estudiante: encapsula el modelo,
el dataset y la métrica de respuesta usados para simular una superficie de
respuesta real.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score

# Rangos naturales de los factores expuestos al estudiante.
X1_RANGE = (0.01, 0.30)  # learning_rate
X2_RANGE = (2, 10)  # max_depth

CSV_COLUMNS = ["corrida", "x1_real", "x2_real", "x1_cod", "x2_cod", "semilla", "y"]

_DATA = load_diabetes(return_X_y=True)


def to_coded(x_real: float, low: float, high: float) -> float:
    center = (low + high) / 2
    half = (high - low) / 2
    return (x_real - center) / half


def to_real(x_coded: float, low: float, high: float) -> float:
    center = (low + high) / 2
    half = (high - low) / 2
    return center + x_coded * half


def validate_ranges(x1_real: float, x2_real: float) -> str | None:
    """Devuelve un mensaje de error si algún factor está fuera de rango, o None si es válido."""
    if not (X1_RANGE[0] <= x1_real <= X1_RANGE[1]):
        return (
            f"x1 (learning_rate) = {x1_real} está fuera de rango. "
            f"Rango válido: [{X1_RANGE[0]}, {X1_RANGE[1]}]."
        )
    if not (X2_RANGE[0] <= x2_real <= X2_RANGE[1]):
        return (
            f"x2 (max_depth) = {x2_real} está fuera de rango. "
            f"Rango válido: [{X2_RANGE[0]}, {X2_RANGE[1]}]."
        )
    return None


def run_experiment(x1_real: float, x2_real_int: int, semilla: int) -> float:
    """Entrena el modelo y devuelve la métrica de respuesta y (R² promedio en CV 5-fold)."""
    X, y = _DATA
    model = GradientBoostingRegressor(
        learning_rate=x1_real,
        max_depth=x2_real_int,
        random_state=semilla,
    )
    cv = KFold(n_splits=5, shuffle=True, random_state=semilla)
    scores = cross_val_score(model, X, y, cv=cv, scoring="r2")
    return float(scores.mean())


def next_corrida_number(csv_path: Path) -> int:
    if not csv_path.exists():
        return 1
    df = pd.read_csv(csv_path)
    if df.empty:
        return 1
    return int(df["corrida"].max()) + 1


def append_result(csv_path: Path, row: dict) -> None:
    df_row = pd.DataFrame([row], columns=CSV_COLUMNS)
    write_header = not csv_path.exists()
    df_row.to_csv(csv_path, mode="a", header=write_header, index=False)


def load_history(csv_path: Path) -> pd.DataFrame | None:
    if not csv_path.exists():
        return None
    return pd.read_csv(csv_path)
