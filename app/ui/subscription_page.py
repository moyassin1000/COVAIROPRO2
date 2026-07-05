"""Subscription status and mock upgrade page."""
from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from app.database.repositories import UserRepository
from app.subscriptions.service import SubscriptionService


class SubscriptionPage(QWidget):
    def __init__(self, app_window) -> None:
        super().__init__()
        self.app_window = app_window
        self.status = QLabel("")
        self._build()
        self.refresh()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        title = QLabel(self.app_window.tr.t("subscription"))
        title.setObjectName("Title")
        layout.addWidget(title)
        card = QFrame()
        card.setObjectName("Card")
        inner = QVBoxLayout(card)
        inner.setContentsMargins(20, 20, 20, 20)
        inner.addWidget(self.status)
        subscribe = QPushButton(self.app_window.tr.t("subscribe_now"))
        subscribe.setObjectName("SuccessButton")
        subscribe.clicked.connect(self.mock_subscribe)
        inner.addWidget(subscribe)
        hint = QLabel(self.app_window.tr.t("subscription_hint"))
        hint.setWordWrap(True)
        inner.addWidget(hint)
        layout.addWidget(card)
        layout.addStretch(1)

    def refresh(self) -> None:
        user = self.app_window.session.user
        if user:
            self.status.setText(f"{self.app_window.tr.t('current_plan')}: {user.get('role')}")

    def mock_subscribe(self) -> None:
        user = self.app_window.session.user
        if not user:
            return
        SubscriptionService(self.app_window.db).activate_mock_premium(int(user["id"]))
        refreshed = UserRepository(self.app_window.db).by_id(int(user["id"]))
        if refreshed:
            self.app_window.session.user = refreshed
        self.refresh()
        self.app_window.refresh_shell_user_label()
