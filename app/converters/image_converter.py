"""Image conversion using Pillow."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

from app.converters.base import ConversionError, ProgressCallback
from app.utils.file_utils import safe_output_path


class ImageConverter:
    def convert(
        self,
        input_path: Path,
        output_dir: Path,
        output_format: str,
        progress: ProgressCallback | None = None,
    ) -> Path:
        output_format = output_format.lower().lstrip(".")
        output_path = safe_output_path(input_path, output_dir, output_format)
        try:
            if progress:
                progress(20, "Opening image...")
            with Image.open(input_path) as image:
                if output_format in {"jpg", "jpeg", "ico"} and image.mode in {"RGBA", "P"}:
                    image = image.convert("RGB")
                if progress:
                    progress(70, "Saving image...")
                pil_format = "JPEG" if output_format in {"jpg", "jpeg"} else output_format.upper()
                image.save(output_path, format=pil_format)
            if progress:
                progress(100, "Done")
            return output_path
        except Exception as exc:
            raise ConversionError(str(exc)) from exc
