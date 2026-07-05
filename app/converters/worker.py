"""Background QThread worker for conversions."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QThread, Signal

from app.database.db import Database
from app.services.conversion_service import ConversionService


class ConversionWorker(QThread):
    progress_changed = Signal(int, str)
    finished_success = Signal(list)
    failed = Signal(str)
    cancelled = Signal()

    def __init__(
        self,
        db: Database,
        user: dict,
        files: list[Path],
        conversion_type: str,
        output_format: str,
        output_dir: Path,
    ) -> None:
        super().__init__()
        self.db = db
        self.user = user
        self.files = files
        self.conversion_type = conversion_type
        self.output_format = output_format
        self.output_dir = output_dir
        self._cancelled = False
        self.service = ConversionService(db)

    def run(self) -> None:
        try:
            results = self.service.convert_files(
                self.user,
                self.files,
                self.conversion_type,
                self.output_format,
                self.output_dir,
                self.progress_changed.emit,
                lambda: self._cancelled,
            )
            if self._cancelled:
                self.cancelled.emit()
            else:
                self.finished_success.emit([str(path) for path in results])
        except Exception as exc:
            if self._cancelled:
                self.cancelled.emit()
            else:
                self.failed.emit(str(exc))

    def cancel(self) -> None:
        self._cancelled = True
        self.service.cancel()
