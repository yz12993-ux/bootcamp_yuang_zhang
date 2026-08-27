"""Feature-engineering helpers for Stage 09."""

import numpy as np
import pandas as pd


def add_income_log(frame: pd.DataFrame, column: str = "income") -> pd.DataFrame:
    """Add ``income_log`` using log1p after validating nonnegative inputs."""
    result = frame.copy()
    if column not in result:
        raise KeyError(column)
    if (result[column].dropna() < 0).any():
        raise ValueError("Log income feature requires nonnegative values")
    result["income_log"] = np.log1p(result[column])
    return result


def add_lagged_transaction_mean(
    frame: pd.DataFrame,
    *,
    value_column: str = "transactions",
    date_column: str = "date",
    window: int = 7,
) -> pd.DataFrame:
    """Add a past-only rolling mean; current-row information is excluded by shift(1)."""
    if window < 2:
        raise ValueError("window must be at least 2")
    result = frame.sort_values(date_column).copy()
    result[f"{value_column}_{window}d_mean_lag1"] = (
        result[value_column].shift(1).rolling(window, min_periods=max(2, window // 2)).mean()
    )
    return result


def encode_region_one_hot(frame: pd.DataFrame, column: str = "region") -> pd.DataFrame:
    """One-hot encode an unordered categorical region without imposing fake rank."""
    if column not in frame:
        raise KeyError(column)
    return pd.get_dummies(frame, columns=[column], prefix=column, dtype=int)
