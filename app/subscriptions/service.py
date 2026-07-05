"""Mock subscription service ready for payment gateway integration."""
from __future__ import annotations

from app.core.config import AppConfig
from app.database.db import Database
from app.database.repositories import ConversionRepository, UserRepository


class SubscriptionLimitError(Exception):
    pass


class SubscriptionService:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.conversions = ConversionRepository(db)

    def daily_limit_for(self, user: dict) -> int:
        role = user.get("role", "Free")
        if role == "Admin":
            return AppConfig.ADMIN_DAILY_LIMIT
        if role == "Premium":
            return AppConfig.PREMIUM_DAILY_LIMIT
        return AppConfig.FREE_DAILY_LIMIT

    def can_convert(self, user: dict) -> tuple[bool, str]:
        if not user.get("is_active", 1):
            return False, "Account is disabled."
        used = self.conversions.count_today_for_user(int(user["id"]))
        limit = self.daily_limit_for(user)
        if used >= limit:
            return False, "Daily conversion limit reached. Subscribe to increase your limit."
        return True, "OK"

    def activate_mock_premium(self, user_id: int) -> None:
        self.users.update_role(user_id, "Premium")

    def set_role(self, user_id: int, role: str) -> None:
        if role not in {"Free", "Premium", "Admin"}:
            raise ValueError("Invalid role")
        self.users.update_role(user_id, role)
