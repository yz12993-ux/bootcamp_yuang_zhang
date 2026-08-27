# Source and chart notes

- Source: seeded, self-contained synthetic monthly scenario data generated in the Stage 12 notebook. No external market data is represented.
- Time window: January-December 2025, monthly grain, 12 observations per scenario.
- Return metric: compounded annual return over the 12 monthly observations.
- Volatility metric: sample standard deviation of monthly returns times square root of 12.
- Chart map:
  - Risk-return scatter: relationship; monthly return vs trailing 3-month annualized volatility; 30 scenario-month observations after warm-up.
  - Cumulative wealth line: trend; growth of $1 over 12 monthly points for three scenarios.
  - Annual return bar: category comparison; compounded return for three scenarios, with a zero baseline and direct value labels.
