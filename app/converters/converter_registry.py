"""Maps conversion types to converter implementations."""
from __future__ import annotations

from app.converters.document_converter import DocumentConverter
from app.converters.ffmpeg_converter import FFmpegConverter
from app.converters.image_converter import ImageConverter
from app.converters.pdf_converter import PDFConverter


class ConverterRegistry:
    def __init__(self) -> None:
        self.ffmpeg = FFmpegConverter()
        self._items = {
            "Documents": DocumentConverter(),
            "PDF": PDFConverter(),
            "Images": ImageConverter(),
            "Videos": self.ffmpeg,
            "Audio": self.ffmpeg,
        }

    def get(self, conversion_type: str):
        return self._items[conversion_type]

    def cancel(self) -> None:
        self.ffmpeg.cancel()
