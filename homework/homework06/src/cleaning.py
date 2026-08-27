"""Reusable, non-mutating cleaning functions for Stage 06."""

from collections.abc import Iterable

import numpy as np
import pandas as pd


def _columns(frame: pd.DataFrame, columns: Iterable[str] | None) -> list[str]:
    selected = list(columns) if columns is not None else frame.select_dtypes(include="number").columns.tolist()
    missing = sorted(set(selected) - set(frame.columns))
    if missing:
        raise KeyError(f"Columns not found: {missing}")
    return selected


def fill_missing_median(frame: pd.DataFrame, columns: Iterable[str] | None = None) -> pd.DataFrame:
    """Return a copy with numeric missing values filled by column medians."""
    result = frame.copy()
    for column in _columns(result, columns):
        if not pd.api.types.is_numeric_dtype(result[column]):
            raise TypeError(f"Median imputation requires a numeric column: {column}")
        median = result[column].median()
        if pd.isna(median):
            raise ValueError(f"Cannot impute all-missing column: {column}")
        result[column] = result[column].fillna(median)
    return result


def drop_missing(
    frame: pd.DataFrame,
    *,
    subset: Iterable[str] | None = None,
    column_threshold: float = 1.0,
) -> pd.DataFrame:
    """Drop columns above a missing-rate threshold, then incomplete rows in ``subset``.

    ``column_threshold`` is inclusive on the kept side: a column is dropped only
    when its missing fraction is strictly greater than the threshold.
    """
    if not 0 <= column_threshold <= 1:
        raise ValueError("column_threshold must be between 0 and 1")
    result = frame.copy()
    missing_rate = result.isna().mean()
    result = result.drop(columns=missing_rate[missing_rate > column_threshold].index)
    if subset is not None:
        row_subset = list(subset)
        missing = sorted(set(row_subset) - set(result.columns))
        if missing:
            raise KeyError(f"Subset columns not found after column drop: {missing}")
        result = result.dropna(subset=row_subset)
    return result.reset_index(drop=True)


def normalize_data(
    frame: pd.DataFrame,
    columns: Iterable[str] | None = None,
    *,
    suffix: str = "_scaled",
) -> pd.DataFrame:
    """Add min-max-scaled columns in [0, 1] without overwriting raw values."""
    result = frame.copy()
    for column in _columns(result, columns):
        if not pd.api.types.is_numeric_dtype(result[column]):
            raise TypeError(f"Normalization requires a numeric column: {column}")
        minimum, maximum = result[column].min(), result[column].max()
        output = f"{column}{suffix}"
        if pd.isna(minimum) or pd.isna(maximum):
            raise ValueError(f"Cannot normalize all-missing column: {column}")
        if np.isclose(maximum, minimum):
            result[output] = 0.0
        else:
            result[output] = (result[column] - minimum) / (maximum - minimum)
    return result
