"""High-level conversion orchestration."""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from app.converters.converter_registry import ConverterRegistry
from app.database.db import Database
from app.database.repositories import ConversionRepository
from app.services.logging_service import get_logger
from app.subscriptions.service import SubscriptionLimitError, SubscriptionService


class ConversionService:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.repo = ConversionRepository(db)
        self.subscriptions = SubscriptionService(db)
        self.registry = ConverterRegistry()
        self.logger = get_logger(__name__)

    def convert_files(
        self,
        user: dict,
        files: list[Path],
        conversion_type: str,
        output_format: str,
        output_dir: Path,
        progress: Callable[[int, str], None] | None = None,
        should_cancel: Callable[[], bool] | None = None,
    ) -> list[Path]:
        allowed, message = self.subscriptions.can_convert(user)
        if not allowed:
            raise SubscriptionLimitError(message)

        converter = self.registry.get(conversion_type)
        results: list[Path] = []
        total = max(len(files), 1)
        for idx, input_path in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            conversion_id = self.repo.create(int(user["id"]), str(input_path), conversion_type, output_format)
            self.repo.mark_started(conversion_id)

            def item_progress(value: int, message: str) -> None:
                combined = int(((idx - 1) / total) * 100 + (value / total))
                if progress:
                    progress(min(combined, 99), f"{input_path.name}: {message}")

            try:
                output_path = converter.convert(input_path, output_dir, output_format, item_progress)
                self.repo.mark_success(conversion_id, str(output_path))
                results.append(output_path)
            except Exception as exc:
                self.repo.mark_error(conversion_id, str(exc))
                self.logger.exception("Conversion failed for %s", input_path)
                raise
        if progress:
            progress(100, "All conversions finished")
        return results

    def cancel(self) -> None:
        self.registry.cancel()
