"""Simple JSON-based translation service."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt

from app.core.config import AppConfig


class Translator:
    def __init__(self, language: str | None = None) -> None:
        self.language = language or AppConfig.DEFAULT_LANGUAGE
        self._cache: dict[str, dict[str, Any]] = {}

    def set_language(self, language: str) -> None:
        if language not in AppConfig.SUPPORTED_LANGUAGES:
            language = AppConfig.DEFAULT_LANGUAGE
        self.language = language

    def direction(self) -> Qt.LayoutDirection:
        return Qt.RightToLeft if self.language == "ar" else Qt.LeftToRight

    def t(self, key: str, **kwargs: Any) -> str:
        data = self._load(self.language)
        value = data.get(key, key)
        if kwargs:
            try:
                return value.format(**kwargs)
            except Exception:
                return value
        return value

    def _load(self, language: str) -> dict[str, Any]:
        if language in self._cache:
            return self._cache[language]
        path = Path(AppConfig.translations_dir()) / f"{language}.json"
        if not path.exists():
            return {}
        self._cache[language] = json.loads(path.read_text(encoding="utf-8"))
        return self._cache[language]
