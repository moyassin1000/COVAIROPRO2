"""Role based permission helpers."""
from __future__ import annotations


def is_admin(user: dict | None) -> bool:
    return bool(user and user.get("role") == "Admin")


def can_use_admin_panel(user: dict | None) -> bool:
    return is_admin(user) and bool(user.get("is_active", 1))


def is_premium(user: dict | None) -> bool:
    return bool(user and user.get("role") in {"Premium", "Admin"})
