# Homework 04 - Data Acquisition and Ingestion

The executed notebook pulls recent AAPL daily market data from Yahoo Finance's public chart endpoint and scrapes the S&P 500 constituents table from Wikipedia. It validates schemas, types, missing values, duplicates, and basic domain rules before saving timestamped raw CSV files under `data/raw/`.

`.env` is ignored. The committed template is `.env.example`; this workflow does not require a secret API key.
