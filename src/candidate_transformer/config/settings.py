"""
Configuration management for the application.

This module is responsible for loading and providing
application configuration.
"""

import json
from pathlib import Path
from typing import Any


def load_config(config_path: Path) -> dict[str, Any]:
    """Load configuration from a JSON file."""
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    if not config_path.is_file():
        raise ValueError(f"Config path is not a file: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)