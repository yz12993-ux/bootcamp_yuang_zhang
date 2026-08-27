# Homework 07 - Outliers and Risk Assumptions

The executed notebook generates the starter's seeded daily-return dataset, improves the IQR/z-score/winsorization helpers in `src/outliers.py`, creates outlier flags, and compares raw, IQR-filtered, and winsorized summaries and regressions. Outputs are saved under `data/processed/`.

Outlier flags are diagnostic evidence, not automatic deletion rules. The five injected May shocks may represent true market events; filtering them changes the population and understates tail risk if those events are relevant to the decision.
