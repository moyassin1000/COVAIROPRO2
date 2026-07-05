"""Document conversion using LibreOffice headless mode."""
from __future__ import annotations

import subprocess
from pathlib import Path

from app.converters.base import ConversionError, ProgressCallback
from app.utils.file_utils import safe_output_path


class DocumentConverter:
    def convert(
        self,
        input_path: Path,
        output_dir: Path,
        output_format: str,
        progress: ProgressCallback | None = None,
    ) -> Path:
        if output_format.lower() != "pdf":
            raise ConversionError("Documents currently support conversion to PDF only.")
        output_path = safe_output_path(input_path, output_dir, "pdf")
        temp_dir = output_dir / ".tmp_libreoffice"
        temp_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(temp_dir),
            str(input_path),
        ]
        try:
            if progress:
                progress(20, "Starting LibreOffice...")
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
                timeout=180,
            )
            if process.returncode != 0:
                raise ConversionError(process.stderr.strip() or "LibreOffice conversion failed.")
            produced = temp_dir / f"{input_path.stem}.pdf"
            if not produced.exists():
                candidates = list(temp_dir.glob("*.pdf"))
                if not candidates:
                    raise ConversionError("LibreOffice did not produce a PDF file.")
                produced = candidates[0]
            produced.replace(output_path)
            if progress:
                progress(100, "Done")
            return output_path
        except FileNotFoundError as exc:
            raise ConversionError("LibreOffice soffice.exe is not installed or not in PATH.") from exc
        except subprocess.TimeoutExpired as exc:
            raise ConversionError("LibreOffice conversion timed out.") from exc
