"""Splash screen."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QSplashScreen

from app.core.config import AppConfig


class SplashScreen(QSplashScreen):
    def __init__(self) -> None:
        pixmap = QPixmap(620, 340)
        pixmap.fill(QColor("#111827"))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor("#ffffff"))
        font = QFont("Segoe UI", 30, QFont.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, AppConfig.APP_NAME)
        painter.setFont(QFont("Segoe UI", 11))
        painter.setPen(QColor("#cbd5e1"))
        painter.drawText(0, 220, 620, 60, Qt.AlignCenter, "Smart file conversion for Windows")
        painter.end()
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
