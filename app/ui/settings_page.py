"""Settings page."""
from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from app.core.config import AppConfig


class SettingsPage(QWidget):
    def __init__(self, app_window) -> None:
        super().__init__()
        self.app_window = app_window
        self.lang_combo = QComboBox()
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)
        title = QLabel(self.app_window.tr.t("settings"))
        title.setObjectName("Title")
        layout.addWidget(title)

        card = QFrame()
        card.setObjectName("Card")
        inner = QVBoxLayout(card)
        inner.setContentsMargins(20, 20, 20, 20)
        inner.addWidget(QLabel(self.app_window.tr.t("language")))
        for code, name in AppConfig.SUPPORTED_LANGUAGES.items():
            self.lang_combo.addItem(name, code)
        index = self.lang_combo.findData(self.app_window.tr.language)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
        inner.addWidget(self.lang_combo)
        apply_btn = QPushButton(self.app_window.tr.t("apply_language"))
        apply_btn.setObjectName("PrimaryButton")
        apply_btn.clicked.connect(self.apply_language)
        inner.addWidget(apply_btn)
        layout.addWidget(card)
        layout.addStretch(1)

    def apply_language(self) -> None:
        self.app_window.change_language(self.lang_combo.currentData())
