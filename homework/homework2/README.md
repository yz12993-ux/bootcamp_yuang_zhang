# Daily Category Value Monitoring - Project Setup

This reproducible Python project prepares the local tooling for the Daily Category Value Monitoring analysis. It separates source data, reusable code, and notebooks; reads local configuration from an ignored `.env` file; and verifies that NumPy and python-dotenv are available in Jupyter. The project intentionally uses a dummy API key only, so no real secret is stored in version control.

## Run locally

1. Create and activate an environment, for example `python -m venv env`.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and keep the supplied dummy values.
4. Start Jupyter and run `notebooks/00_project_setup.ipynb` from top to bottom.

## Structure

- `data/` - raw and processed data
- `notebooks/` - executable checks and analysis
- `src/` - reusable configuration code
