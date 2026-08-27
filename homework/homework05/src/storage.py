"""Reusable DataFrame storage helpers for Stage 05."""

from pathlib import Path
from typing import Iterable, Union

import pandas as pd

PathLike = Union[str, Path]


def detect_format(path: PathLike) -> str:
    """Return ``csv`` or ``parquet`` from a supported path suffix."""
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix in {".parquet", ".pq", ".parq"}:
        return "parquet"
    raise ValueError(f"Unsupported storage format: {suffix or '[no suffix]'}")


def write_df(frame: pd.DataFrame, path: PathLike) -> Path:
    """Write a DataFrame, creating parent directories as needed."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    storage_format = detect_format(destination)
    if storage_format == "csv":
        frame.to_csv(destination, index=False)
    else:
        try:
            frame.to_parquet(destination, index=False)
        except (ImportError, ModuleNotFoundError) as exc:
            raise RuntimeError(
                "Parquet support requires pyarrow or fastparquet. Install one and rerun."
            ) from exc
    return destination


def read_df(path: PathLike, parse_dates: Iterable[str] | None = None) -> pd.DataFrame:
    """Read a supported DataFrame file with a clear missing-file error."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Data file not found: {source}")
    storage_format = detect_format(source)
    if storage_format == "csv":
        return pd.read_csv(source, parse_dates=list(parse_dates or []))
    try:
        return pd.read_parquet(source)
    except (ImportError, ModuleNotFoundError) as exc:
        raise RuntimeError(
            "Parquet support requires pyarrow or fastparquet. Install one and rerun."
        ) from exc
