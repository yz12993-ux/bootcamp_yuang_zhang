"""Reusable exploratory-data-analysis summaries for Stage 08."""

import pandas as pd


def eda_summary(
    frame: pd.DataFrame,
    *,
    high_missing: float = 0.05,
    dominance_threshold: float = 0.90,
) -> dict:
    """Return numeric, categorical, and attention-flag summaries."""
    if frame.empty:
        raise ValueError("Cannot summarize an empty DataFrame")
    if not 0 <= high_missing <= 1 or not 0 <= dominance_threshold <= 1:
        raise ValueError("Thresholds must be between 0 and 1")

    numeric_columns = frame.select_dtypes(include="number").columns
    numeric = frame[numeric_columns].describe().T if len(numeric_columns) else pd.DataFrame()
    if not numeric.empty:
        numeric["missing_count"] = frame[numeric_columns].isna().sum()
        numeric["missing_rate"] = frame[numeric_columns].isna().mean()
        numeric["nunique"] = frame[numeric_columns].nunique(dropna=True)
        numeric["skew"] = frame[numeric_columns].skew(numeric_only=True)
        numeric["kurtosis"] = frame[numeric_columns].kurtosis(numeric_only=True)

    categorical_columns = frame.select_dtypes(include=["object", "category", "bool"]).columns
    categorical_rows = []
    for column in categorical_columns:
        counts = frame[column].value_counts(dropna=False)
        categorical_rows.append({
            "column": column,
            "nunique": frame[column].nunique(dropna=True),
            "missing_count": int(frame[column].isna().sum()),
            "top_value": counts.index[0] if len(counts) else None,
            "top_count": int(counts.iloc[0]) if len(counts) else 0,
            "top_share": float(counts.iloc[0] / len(frame)) if len(counts) else 0.0,
        })
    categorical = pd.DataFrame(categorical_rows).set_index("column") if categorical_rows else pd.DataFrame()

    flags = []
    for column in frame.columns:
        missing_rate = frame[column].isna().mean()
        if missing_rate > high_missing:
            flags.append({"column": column, "issue": "high_missingness", "value": missing_rate})
        if frame[column].nunique(dropna=True) <= 1:
            flags.append({"column": column, "issue": "near_zero_variance", "value": frame[column].nunique(dropna=True)})
    if not categorical.empty:
        for column, row in categorical.iterrows():
            if row["top_share"] > dominance_threshold:
                flags.append({"column": column, "issue": "dominant_category", "value": row["top_share"]})

    return {
        "shape": frame.shape,
        "dtypes": frame.dtypes.astype(str),
        "numeric": numeric,
        "categorical": categorical,
        "attention_flags": pd.DataFrame(flags, columns=["column", "issue", "value"]),
    }
