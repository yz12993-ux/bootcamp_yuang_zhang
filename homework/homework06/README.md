# Homework 06 - Data Preprocessing

## Cleaning strategy

The raw sample is retained under `data/raw/`. The main processed path drops only columns with more than 50% missing values (`extra_data`), median-imputes the three substantive numeric fields (`age`, `income`, `score`), and adds min-max scaled copies while retaining the original units. The completed data is saved to `data/processed/sample_data_cleaned.csv`.

`src/cleaning.py` contains non-mutating, documented helpers. Median imputation assumes the observed values are representative and can reduce variance. Complete-case deletion is shown as a sensitivity alternative and can bias the sample when missingness is systematic. Min-max scaling depends on observed extrema and should be fit on training data only in a later modeling workflow.
