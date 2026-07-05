"""Main application window and navigation shell."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.auth.auth_service import AuthService
from app.auth.session import Session
from app.core.i18n import Translator
from app.core.permissions import can_use_admin_panel
from app.database.db import Database
from app.database.repositories import UserRepository
from app.ui.admin_panel import AdminPanel
from app.ui.dashboard_page import DashboardPage
from app.ui.history_page import HistoryPage
from app.ui.login_page import LoginPage
from app.ui.register_page import RegisterPage
from app.ui.settings_page import SettingsPage
from app.ui.styles import APP_QSS
from app.ui.subscription_page import SubscriptionPage


class AppWindow(QMainWindow):
    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.tr = Translator()
        self.session = Session()
        self.auth = AuthService(db)
        self.stack = QStackedWidget()
        self.shell = None
        self.setMinimumSize(1160, 760)
        self.setStyleSheet(APP_QSS)
        self.setWindowTitle("Convairo Pro")
        self.setCentralWidget(self.stack)
        self.setLayoutDirection(self.tr.direction())
        self.show_login()

    def _clear_stack(self) -> None:
        while self.stack.count():
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()

    def show_login(self) -> None:
        self.session.logout()
        self._clear_stack()
        self.stack.addWidget(LoginPage(self))

    def show_register(self) -> None:
        self._clear_stack()
        self.stack.addWidget(RegisterPage(self))

    def register(self, name: str, email: str, password: str) -> None:
        user = self.auth.register(name, email, password)
        self.session.login(user)
        self.show_shell()

    def login(self, email: str, password: str) -> None:
        user = self.auth.login(email, password)
        self.session.login(user)
        self.show_shell()

    def show_shell(self) -> None:
        self._clear_stack()
        self.shell = MainShell(self)
        self.stack.addWidget(self.shell)

    def logout(self) -> None:
        self.show_login()

    def change_language(self, language: str) -> None:
        self.tr.set_language(language)
        self.setLayoutDirection(self.tr.direction())
        if self.session.user:
            self.show_shell()
        else:
            self.show_login()

    def refresh_history(self) -> None:
        if self.shell:
            self.shell.refresh_history()

    def refresh_shell_user_label(self) -> None:
        if self.shell:
            self.shell.refresh_user_label()


class MainShell(QWidget):
    def __init__(self, app_window: AppWindow) -> None:
        super().__init__()
        self.app_window = app_window
        self.nav = QListWidget()
        self.pages = QStackedWidget()
        self.user_label = QLabel("")
        self.dashboard = DashboardPage(app_window)
        self.history = HistoryPage(app_window)
        self.subscription = SubscriptionPage(app_window)
        self.settings = SettingsPage(app_window)
        self.admin_panel = AdminPanel(app_window) if can_use_admin_panel(app_window.session.user) else None
        self._build()
        self.refresh_user_label()
        self.refresh_history()
        if self.admin_panel:
            self.admin_panel.refresh()

    def _build(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        sidebar = QWidget()
        sidebar.setStyleSheet("background:#111827;")
        sidebar.setFixedWidth(260)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(12, 18, 12, 18)
        app_title = QLabel("Convairo Pro")
        app_title.setStyleSheet("color:white;font-size:22px;font-weight:700;padding:8px;")
        self.user_label.setStyleSheet("color:#cbd5e1;padding:8px;")
        side_layout.addWidget(app_title)
        side_layout.addWidget(self.user_label)
        side_layout.addWidget(self.nav, 1)
        logout_btn = QPushButton(self.app_window.tr.t("logout"))
        logout_btn.clicked.connect(self.app_window.logout)
        side_layout.addWidget(logout_btn)

        items = [
            (self.app_window.tr.t("dashboard"), self.dashboard),
            (self.app_window.tr.t("history"), self.history),
            (self.app_window.tr.t("subscription"), self.subscription),
            (self.app_window.tr.t("settings"), self.settings),
        ]
        if self.admin_panel:
            items.append((self.app_window.tr.t("admin_panel"), self.admin_panel))
        for name, widget in items:
            self.nav.addItem(QListWidgetItem(name))
            self.pages.addWidget(widget)
        self.nav.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.nav.setCurrentRow(0)

        root.addWidget(sidebar)
        root.addWidget(self.pages, 1)

    def refresh_user_label(self) -> None:
        user = self.app_window.session.user or {}
        self.user_label.setText(f"{user.get('name','')}\n{user.get('email','')}\n{self.app_window.tr.t('role')}: {user.get('role','')}")

    def refresh_history(self) -> None:
        self.history.refresh()
        self.dashboard.refresh_stats()
        if self.admin_panel:
            self.admin_panel.refresh()
