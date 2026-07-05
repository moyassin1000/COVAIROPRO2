"""Admin-only operations."""
from __future__ import annotations

from app.core.permissions import can_use_admin_panel
from app.database.db import Database
from app.database.repositories import ConversionRepository, UserRepository


class PermissionDenied(Exception):
    pass


class AdminService:
    def __init__(self, db: Database, current_user: dict | None) -> None:
        if not can_use_admin_panel(current_user):
            raise PermissionDenied("Admin privileges required.")
        self.users = UserRepository(db)
        self.conversions = ConversionRepository(db)

    def users_with_stats(self) -> list[dict]:
        return self.users.list_all()

    def conversions(self) -> list[dict]:
        return self.conversions.list_all()

    def set_user_role(self, user_id: int, role: str) -> None:
        if role not in {"Free", "Premium", "Admin"}:
            raise ValueError("Invalid role")
        self.users.update_role(user_id, role)

    def set_user_active(self, user_id: int, active: bool) -> None:
        self.users.set_active(user_id, active)
