# Homework 05 - Data Storage

## Data Storage

- `data/raw/` stores the portable CSV snapshot. CSV is human-readable and widely supported, but it does not preserve every dtype automatically.
- `data/processed/` stores the Parquet copy. Parquet is columnar, compact, and preserves datetimes and numeric dtypes; it requires `pyarrow` or `fastparquet`.
- `.env` defines `DATA_DIR_RAW=data/raw` and `DATA_DIR_PROCESSED=data/processed`. The notebook loads those values with `python-dotenv`; `.env` is ignored and `.env.example` is the shareable template.
- `src/storage.py` routes `read_df` and `write_df` by suffix, creates missing parent directories, rejects unsupported suffixes, and gives a clear Parquet-engine message.

The executed notebook reloads both formats and checks shape, required columns, datetime/numeric dtypes, ticker values, and price equality.
