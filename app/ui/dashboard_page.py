"""Main conversion dashboard."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QComboBox,
    QProgressBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.converters.worker import ConversionWorker
from app.core.config import AppConfig
from app.core.constants import CONVERSION_TYPES
from app.database.repositories import ConversionRepository
from app.services.dependency_checker import DependencyChecker


class DashboardPage(QWidget):
    def __init__(self, app_window) -> None:
        super().__init__()
        self.app_window = app_window
        self.selected_files: list[Path] = []
        self.output_dir = AppConfig.output_dir()
        self.worker: ConversionWorker | None = None

        self.file_list = QListWidget()
        self.type_combo = QComboBox()
        self.format_combo = QComboBox()
        self.progress = QProgressBar()
        self.status = QLabel("")
        self.output_label = QLabel(str(self.output_dir))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.start_btn = QPushButton(self.app_window.tr.t("start_conversion"))
        self.cancel_btn = QPushButton(self.app_window.tr.t("cancel"))
        self.cancel_btn.setEnabled(False)
        self._build()
        self._refresh_formats()

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(22, 22, 22, 22)
        root.setSpacing(16)

        title = QLabel(self.app_window.tr.t("dashboard"))
        title.setObjectName("Title")
        root.addWidget(title)

        card = QFrame()
        card.setObjectName("Card")
        grid = QGridLayout(card)
        grid.setContentsMargins(20, 20, 20, 20)
        grid.setSpacing(12)

        pick_btn = QPushButton(self.app_window.tr.t("choose_files"))
        pick_btn.setObjectName("PrimaryButton")
        pick_btn.clicked.connect(self.choose_files)
        out_btn = QPushButton(self.app_window.tr.t("choose_output"))
        out_btn.clicked.connect(self.choose_output)

        self.type_combo.addItems(CONVERSION_TYPES.keys())
        self.type_combo.currentTextChanged.connect(self._refresh_formats)

        self.start_btn.setObjectName("SuccessButton")
        self.start_btn.clicked.connect(self.start_conversion)
        self.cancel_btn.setObjectName("DangerButton")
        self.cancel_btn.clicked.connect(self.cancel_conversion)

        grid.addWidget(pick_btn, 0, 0)
        grid.addWidget(out_btn, 0, 1)
        grid.addWidget(QLabel(self.app_window.tr.t("conversion_type")), 1, 0)
        grid.addWidget(self.type_combo, 1, 1)
        grid.addWidget(QLabel(self.app_window.tr.t("output_format")), 2, 0)
        grid.addWidget(self.format_combo, 2, 1)
        grid.addWidget(QLabel(self.app_window.tr.t("output_folder")), 3, 0)
        grid.addWidget(self.output_label, 3, 1)
        grid.addWidget(self.progress, 4, 0, 1, 2)
        grid.addWidget(self.status, 5, 0, 1, 2)

        buttons = QHBoxLayout()
        buttons.addWidget(self.start_btn)
        buttons.addWidget(self.cancel_btn)
        grid.addLayout(buttons, 6, 0, 1, 2)

        root.addWidget(card)
        root.addWidget(QLabel(self.app_window.tr.t("selected_files")))
        root.addWidget(self.file_list, 2)
        root.addWidget(QLabel(self.app_window.tr.t("process_log")))
        root.addWidget(self.log, 1)
        self.show_dependencies_status()

    def _refresh_formats(self) -> None:
        self.format_combo.clear()
        self.format_combo.addItems(CONVERSION_TYPES.get(self.type_combo.currentText(), []))

    def choose_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(self, self.app_window.tr.t("choose_files"))
        if files:
            self.selected_files = [Path(f) for f in files]
            self.file_list.clear()
            self.file_list.addItems([str(f) for f in self.selected_files])

    def choose_output(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, self.app_window.tr.t("choose_output"), str(self.output_dir))
        if folder:
            self.output_dir = Path(folder)
            self.output_label.setText(str(self.output_dir))

    def show_dependencies_status(self) -> None:
        statuses = DependencyChecker.check_all()
        missing = [s for s in statuses if not s.available]
        if missing:
            for dep in missing:
                self.log.append(f"Missing {dep.name}: {dep.hint}")
        else:
            self.log.append("All required external tools are available.")

    def start_conversion(self) -> None:
        if not self.selected_files:
            QMessageBox.warning(self, self.app_window.tr.t("warning"), self.app_window.tr.t("no_files"))
            return
        conversion_type = self.type_combo.currentText()
        missing = DependencyChecker.missing_for_type(conversion_type)
        if missing:
            QMessageBox.warning(self, self.app_window.tr.t("missing_tools"), "\n".join([m.hint for m in missing]))
            return
        self.progress.setValue(0)
        self.log.append("Starting conversion...")
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.worker = ConversionWorker(
            self.app_window.db,
            self.app_window.session.user,
            self.selected_files,
            conversion_type,
            self.format_combo.currentText(),
            self.output_dir,
        )
        self.worker.progress_changed.connect(self._on_progress)
        self.worker.finished_success.connect(self._on_success)
        self.worker.failed.connect(self._on_failed)
        self.worker.cancelled.connect(self._on_cancelled)
        self.worker.start()

    def cancel_conversion(self) -> None:
        if self.worker:
            self.worker.cancel()
            self.status.setText(self.app_window.tr.t("cancelling"))

    def _on_progress(self, value: int, message: str) -> None:
        self.progress.setValue(value)
        self.status.setText(message)
        self.log.append(message)

    def _on_success(self, outputs: list[str]) -> None:
        self.progress.setValue(100)
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.log.append("Finished successfully:")
        for item in outputs:
            self.log.append(item)
        self.app_window.refresh_history()

    def _on_failed(self, message: str) -> None:
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.log.append(f"Error: {message}")
        QMessageBox.critical(self, self.app_window.tr.t("error"), message)
        self.app_window.refresh_history()

    def _on_cancelled(self) -> None:
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.log.append("Conversion cancelled.")

    def refresh_stats(self) -> None:
        if not self.app_window.session.user:
            return
        repo = ConversionRepository(self.app_window.db)
        today = repo.count_today_for_user(int(self.app_window.session.user["id"]))
        role = self.app_window.session.user.get("role", "Free")
        self.status.setText(f"{self.app_window.tr.t('role')}: {role} | Today: {today}")
