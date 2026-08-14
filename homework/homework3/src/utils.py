"""Reusable helpers for the Stage 03 dataset exploration."""

import pandas as pd


def get_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return a readable category-level summary for a value dataset.

    The input must contain `category` and numeric `value` columns.
    """
    required_columns = {"category", "value"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    return (
        df.groupby("category", as_index=False)["value"]
        .agg(count="count", total="sum", mean="mean", minimum="min", maximum="max")
        .sort_values("category")
    )
