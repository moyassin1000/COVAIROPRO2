"""Shared constants."""
from __future__ import annotations

CONVERSION_TYPES = {
    "Documents": ["pdf"],
    "PDF": ["png", "jpg"],
    "Images": ["jpg", "png", "webp", "bmp", "tiff", "ico"],
    "Videos": ["mp4", "mkv", "avi", "mov", "webm"],
    "Audio": ["mp3", "wav", "aac", "m4a", "ogg", "flac"],
}

INPUT_EXTENSIONS = {
    "Documents": ["docx", "doc", "odt", "txt"],
    "PDF": ["pdf"],
    "Images": ["jpg", "jpeg", "png", "webp", "bmp", "tiff", "ico"],
    "Videos": ["mp4", "mkv", "avi", "mov", "webm"],
    "Audio": ["mp3", "wav", "aac", "m4a", "ogg", "flac"],
}

ROLES = ("Free", "Premium", "Admin")
