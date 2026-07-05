"""Application entry point for Convairo Pro."""
from __future__ import annotations

import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from app.core.config import AppConfig
from app.core.paths import ensure_app_directories
from app.database.db import Database
from app.ui.app_window import AppWindow
from app.ui.splash_screen import SplashScreen


def bootstrap_database(db: Database) -> None:
    """Initialize SQLite schema and optionally bootstrap an admin safely.

    First registered user becomes Admin automatically. For CI or enterprise
    deployments, an admin can also be created by setting these env vars before
    first launch:
        CONVAIRO_ADMIN_NAME
        CONVAIRO_ADMIN_EMAIL
        CONVAIRO_ADMIN_PASSWORD
    """
    db.initialize()
    name = os.getenv("CONVAIRO_ADMIN_NAME")
    email = os.getenv("CONVAIRO_ADMIN_EMAIL")
    password = os.getenv("CONVAIRO_ADMIN_PASSWORD")
    if email and password:
        from app.auth.auth_service import AuthService

        auth = AuthService(db)
        if not auth.get_user_by_email(email):
            auth.register(name or "Administrator", email, password, force_role="Admin")


def main() -> int:
    ensure_app_directories()
    db = Database(AppConfig.database_path())
    bootstrap_database(db)

    app = QApplication(sys.argv)
    app.setApplicationName(AppConfig.APP_NAME)
    app.setOrganizationName(AppConfig.ORGANIZATION)

    splash = SplashScreen()
    splash.show()

    window = AppWindow(db)

    def show_main() -> None:
        splash.finish(window)
        window.show()

    QTimer.singleShot(AppConfig.SPLASH_MS, show_main)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
