"""Path helpers."""
from __future__ import annotations

from app.core.config import AppConfig


def ensure_app_directories() -> None:
    for path in [AppConfig.output_dir(), AppConfig.logs_dir()]:
        path.mkdir(parents=True, exist_ok=True)
