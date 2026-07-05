"""Check required external command line tools."""
from __future__ import annotations

import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class DependencyStatus:
    name: str
    executable: str
    available: bool
    hint: str


class DependencyChecker:
    REQUIREMENTS = {
        "FFmpeg": ("ffmpeg", "Install FFmpeg and add it to PATH."),
        "LibreOffice": ("soffice", "Install LibreOffice and add soffice.exe to PATH."),
    }

    @classmethod
    def check_all(cls) -> list[DependencyStatus]:
        statuses: list[DependencyStatus] = []
        for name, (exe, hint) in cls.REQUIREMENTS.items():
            statuses.append(DependencyStatus(name, exe, shutil.which(exe) is not None, hint))
        return statuses

    @classmethod
    def missing_for_type(cls, conversion_type: str) -> list[DependencyStatus]:
        statuses = {s.name: s for s in cls.check_all()}
        if conversion_type in {"Videos", "Audio"}:
            ff = statuses.get("FFmpeg")
            return [ff] if ff and not ff.available else []
        if conversion_type == "Documents":
            lo = statuses.get("LibreOffice")
            return [lo] if lo and not lo.available else []
        return []
