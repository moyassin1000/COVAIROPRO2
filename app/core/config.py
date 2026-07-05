"""Static configuration values for Convairo Pro."""
from __future__ import annotations

from pathlib import Path


class AppConfig:
    APP_NAME = "Convairo Pro"
    ORGANIZATION = "Convairo"
    SPLASH_MS = 1400
    DEFAULT_LANGUAGE = "ar"

    FREE_DAILY_LIMIT = 10
    PREMIUM_DAILY_LIMIT = 10_000
    ADMIN_DAILY_LIMIT = 100_000

    SUPPORTED_LANGUAGES = {
        "ar": "العربية",
        "en": "English",
    }

    @staticmethod
    def project_root() -> Path:
        return Path(__file__).resolve().parents[2]

    @staticmethod
    def database_path() -> Path:
        return AppConfig.project_root() / "app_data.sqlite3"

    @staticmethod
    def output_dir() -> Path:
        return AppConfig.project_root() / "output"

    @staticmethod
    def logs_dir() -> Path:
        return AppConfig.project_root() / "logs"

    @staticmethod
    def translations_dir() -> Path:
        return AppConfig.project_root() / "app" / "translations"

    @staticmethod
    def assets_dir() -> Path:
        return AppConfig.project_root() / "assets"
