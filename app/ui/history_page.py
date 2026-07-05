"""Conversion history page."""
from __future__ import annotations

from PySide6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from app.database.repositories import ConversionRepository


class HistoryPage(QWidget):
    def __init__(self, app_window) -> None:
        super().__init__()
        self.app_window = app_window
        self.table = QTableWidget(0, 7)
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        title = QLabel(self.app_window.tr.t("history"))
        title.setObjectName("Title")
        layout.addWidget(title)
        self.table.setHorizontalHeaderLabels([
            "ID", "Source", "Output", "Type", "Format", "Status", "Created",
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

    def refresh(self) -> None:
        user = self.app_window.session.user
        if not user:
            return
        rows = ConversionRepository(self.app_window.db).list_for_user(int(user["id"]))
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            values = [
                row.get("id"), row.get("source_path"), row.get("output_path"),
                row.get("conversion_type"), row.get("output_format"), row.get("status"), row.get("created_at"),
            ]
            for c, value in enumerate(values):
                self.table.setItem(r, c, QTableWidgetItem(str(value or "")))
