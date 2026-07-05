"""File handling utilities."""
from __future__ import annotations

from pathlib import Path


def safe_output_path(input_path: Path, output_dir: Path, extension: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    base = input_path.stem
    extension = extension.lower().lstrip(".")
    candidate = output_dir / f"{base}.{extension}"
    if not candidate.exists():
        return candidate
    for i in range(1, 10_000):
        candidate = output_dir / f"{base}_{i}.{extension}"
        if not candidate.exists():
            return candidate
    raise RuntimeError("Could not create a unique output filename.")
