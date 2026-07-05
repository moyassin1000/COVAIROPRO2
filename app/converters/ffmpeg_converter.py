"""Video and audio conversion powered by FFmpeg."""
from __future__ import annotations

import subprocess
from pathlib import Path

from app.converters.base import ConversionError, ProgressCallback
from app.utils.file_utils import safe_output_path


class FFmpegConverter:
    def __init__(self) -> None:
        self._process: subprocess.Popen | None = None

    def convert(
        self,
        input_path: Path,
        output_dir: Path,
        output_format: str,
        progress: ProgressCallback | None = None,
    ) -> Path:
        output_path = safe_output_path(input_path, output_dir, output_format)
        if progress:
            progress(5, "Preparing FFmpeg conversion...")
        cmd = ["ffmpeg", "-y", "-i", str(input_path), str(output_path)]
        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
            )
            _stdout, stderr = self._process.communicate()
            if self._process.returncode != 0:
                raise ConversionError(stderr.strip() or "FFmpeg conversion failed.")
            if progress:
                progress(100, "Done")
            return output_path
        except FileNotFoundError as exc:
            raise ConversionError("FFmpeg is not installed or not available in PATH.") from exc
        finally:
            self._process = None

    def cancel(self) -> None:
        if self._process and self._process.poll() is None:
            self._process.terminate()
