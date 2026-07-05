"""PDF conversion helpers."""
from __future__ import annotations

from pathlib import Path

from app.converters.base import ConversionError, ProgressCallback


class PDFConverter:
    def convert(
        self,
        input_path: Path,
        output_dir: Path,
        output_format: str,
        progress: ProgressCallback | None = None,
    ) -> Path:
        output_format = output_format.lower().lstrip(".")
        if output_format not in {"png", "jpg", "jpeg"}:
            raise ConversionError("PDF output format must be PNG or JPG.")
        try:
            from pdf2image import convert_from_path
        except Exception as exc:
            raise ConversionError("pdf2image is missing. Install it and Poppler for Windows.") from exc

        output_dir.mkdir(parents=True, exist_ok=True)
        if progress:
            progress(10, "Rendering PDF pages...")
        pages = convert_from_path(str(input_path), dpi=200)
        first_path: Path | None = None
        total = max(len(pages), 1)
        for index, page in enumerate(pages, start=1):
            path = output_dir / f"{input_path.stem}_page_{index}.{output_format}"
            if output_format in {"jpg", "jpeg"} and page.mode != "RGB":
                page = page.convert("RGB")
            page.save(path)
            first_path = first_path or path
            if progress:
                progress(10 + int(index / total * 90), f"Saved page {index}/{total}")
        if not first_path:
            raise ConversionError("No pages were rendered from the PDF.")
        return first_path
