"""Base converter interfaces."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Protocol

ProgressCallback = Callable[[int, str], None]


class Converter(Protocol):
    def convert(
        self,
        input_path: Path,
        output_dir: Path,
        output_format: str,
        progress: ProgressCallback | None = None,
    ) -> Path:
        ...


class ConversionError(Exception):
    pass
