"""Small helpers for reading local project configuration safely."""

from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_env() -> bool:
    """Load this project's local .env file and return whether it was found."""
    env_path = PROJECT_ROOT / ".env"
    return load_dotenv(env_path, override=False)


def get_key() -> str | None:
    """Return the configured API key, or None when it has not been set."""
    return os.getenv("API_KEY")
