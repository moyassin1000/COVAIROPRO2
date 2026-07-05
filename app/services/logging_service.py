"""Application logging setup."""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from app.core.config import AppConfig


def get_logger(name: str = "convairo") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    AppConfig.logs_dir().mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        AppConfig.logs_dir() / "convairo.log",
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
