"""Login page."""
from __future__ import annotations

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class LoginPage(QWidget):
    def __init__(self, app_window) -> None:
        super().__init__()
        self.app_window = app_window
        self.email = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.message = QLabel("")
        self.message.setStyleSheet("color:#dc2626;")
        self._build()

    def _build(self) -> None:
        root = QHBoxLayout(self)
        root.addStretch(1)
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(430)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(14)

        title = QLabel(self.app_window.tr.t("login_title"))
        title.setObjectName("Title")
        subtitle = QLabel(self.app_window.tr.t("login_subtitle"))
        subtitle.setObjectName("Subtitle")
        self.email.setPlaceholderText(self.app_window.tr.t("email"))
        self.password.setPlaceholderText(self.app_window.tr.t("password"))

        login_btn = QPushButton(self.app_window.tr.t("login"))
        login_btn.setObjectName("PrimaryButton")
        login_btn.clicked.connect(self._login)
        register_btn = QPushButton(self.app_window.tr.t("create_account"))
        register_btn.clicked.connect(self.app_window.show_register)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)
        layout.addWidget(self.message)
        root.addWidget(card)
        root.addStretch(1)

    def _login(self) -> None:
        try:
            self.app_window.login(self.email.text(), self.password.text())
        except Exception as exc:
            self.message.setText(str(exc))
