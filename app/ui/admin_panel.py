"""Admin dashboard UI."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.admin.admin_service import AdminService, PermissionDenied
from app.core.constants import ROLES


class AdminPanel(QWidget):
    def __init__(self, app_window) -> None:
        super().__init__()
        self.app_window = app_window
        self.users_table = QTableWidget(0, 7)
        self.logs_table = QTableWidget(0, 8)
        self.role_combo = QComboBox()
        self.role_combo.addItems(ROLES)
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        title = QLabel(self.app_window.tr.t("admin_panel"))
        title.setObjectName("Title")
        layout.addWidget(title)

        actions = QHBoxLayout()
        actions.addWidget(QLabel(self.app_window.tr.t("change_role")))
        actions.addWidget(self.role_combo)
        apply_role = QPushButton(self.app_window.tr.t("apply"))
        apply_role.setObjectName("PrimaryButton")
        apply_role.clicked.connect(self.apply_role)
        disable = QPushButton(self.app_window.tr.t("toggle_active"))
        disable.clicked.connect(self.toggle_active)
        refresh = QPushButton(self.app_window.tr.t("refresh"))
        refresh.clicked.connect(self.refresh)
        actions.addWidget(apply_role)
        actions.addWidget(disable)
        actions.addWidget(refresh)
        actions.addStretch(1)
        layout.addLayout(actions)

        self.users_table.setHorizontalHeaderLabels([
            "ID", "Name", "Email", "Role", "Active", "Registered", "Conversions",
        ])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(QLabel(self.app_window.tr.t("users")))
        layout.addWidget(self.users_table, 2)

        self.logs_table.setHorizontalHeaderLabels([
            "ID", "User", "Email", "Source", "Output", "Type", "Status", "Created",
        ])
        self.logs_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(QLabel(self.app_window.tr.t("operations")))
        layout.addWidget(self.logs_table, 2)

    def _service(self) -> AdminService | None:
        try:
            return AdminService(self.app_window.db, self.app_window.session.user)
        except PermissionDenied:
            return None

    def refresh(self) -> None:
        service = self._service()
        if not service:
            return
        users = service.users_with_stats()
        self.users_table.setRowCount(len(users))
        for r, row in enumerate(users):
            values = [
                row.get("id"), row.get("name"), row.get("email"), row.get("role"),
                row.get("is_active"), row.get("created_at"), row.get("conversion_count"),
            ]
            for c, value in enumerate(values):
                self.users_table.setItem(r, c, QTableWidgetItem(str(value or "")))

        logs = service.conversions()
        self.logs_table.setRowCount(len(logs))
        for r, row in enumerate(logs):
            values = [
                row.get("id"), row.get("name"), row.get("email"), row.get("source_path"),
                row.get("output_path"), row.get("conversion_type"), row.get("status"), row.get("created_at"),
            ]
            for c, value in enumerate(values):
                self.logs_table.setItem(r, c, QTableWidgetItem(str(value or "")))

    def selected_user_id(self) -> int | None:
        row = self.users_table.currentRow()
        if row < 0:
            return None
        item = self.users_table.item(row, 0)
        return int(item.text()) if item else None

    def apply_role(self) -> None:
        user_id = self.selected_user_id()
        service = self._service()
        if user_id and service:
            service.set_user_role(user_id, self.role_combo.currentText())
            self.refresh()

    def toggle_active(self) -> None:
        row = self.users_table.currentRow()
        user_id = self.selected_user_id()
        service = self._service()
        if user_id and service and row >= 0:
            active_item = self.users_table.item(row, 4)
            active = active_item.text() == "1" if active_item else True
            service.set_user_active(user_id, not active)
            self.refresh()
