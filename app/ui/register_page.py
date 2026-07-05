"""Registration page."""
from __future__ import annotations

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class RegisterPage(QWidget):
    def __init__(self, app_window) -> None:
        super().__init__()
        self.app_window = app_window
        self.name = QLineEdit()
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
        card.setFixedWidth(450)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(14)

        title = QLabel(self.app_window.tr.t("register_title"))
        title.setObjectName("Title")
        subtitle = QLabel(self.app_window.tr.t("register_subtitle"))
        subtitle.setObjectName("Subtitle")
        self.name.setPlaceholderText(self.app_window.tr.t("name"))
        self.email.setPlaceholderText(self.app_window.tr.t("email"))
        self.password.setPlaceholderText(self.app_window.tr.t("password"))

        register_btn = QPushButton(self.app_window.tr.t("register"))
        register_btn.setObjectName("PrimaryButton")
        register_btn.clicked.connect(self._register)
        login_btn = QPushButton(self.app_window.tr.t("back_to_login"))
        login_btn.clicked.connect(self.app_window.show_login)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self.name)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(register_btn)
        layout.addWidget(login_btn)
        layout.addWidget(self.message)
        root.addWidget(card)
        root.addStretch(1)

    def _register(self) -> None:
        try:
            self.app_window.register(self.name.text(), self.email.text(), self.password.text())
        except Exception as exc:
            self.message.setText(str(exc))
