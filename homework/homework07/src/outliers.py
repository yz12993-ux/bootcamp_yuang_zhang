"""Outlier detection and treatment helpers for Stage 07."""

import numpy as np
import pandas as pd


def _numeric_series(series: pd.Series) -> pd.Series:
    if not isinstance(series, pd.Series):
        raise TypeError("Expected a pandas Series")
    if series.empty:
        raise ValueError("Series must not be empty")
    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError("Outlier detection requires numeric data")
    return series


def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """Flag values outside Q1 - k*IQR and Q3 + k*IQR; NaNs are unflagged."""
    values = _numeric_series(series)
    if k <= 0:
        raise ValueError("k must be positive")
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    mask = (values < q1 - k * iqr) | (values > q3 + k * iqr)
    return mask.fillna(False)


def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """Flag absolute population z-scores above ``threshold``; NaNs are unflagged."""
    values = _numeric_series(series)
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    sigma = values.std(ddof=0)
    if pd.isna(sigma) or np.isclose(sigma, 0):
        return pd.Series(False, index=values.index)
    zscore = (values - values.mean()) / sigma
    return zscore.abs().gt(threshold).fillna(False)


def winsorize_series(series: pd.Series, lower: float = 0.05, upper: float = 0.95) -> pd.Series:
    """Clip values to empirical lower/upper quantiles while preserving NaNs."""
    values = _numeric_series(series)
    if not 0 <= lower < upper <= 1:
        raise ValueError("Require 0 <= lower < upper <= 1")
    low_value, high_value = values.quantile([lower, upper])
    return values.clip(lower=low_value, upper=high_value)
