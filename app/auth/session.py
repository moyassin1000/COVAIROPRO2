"""Current authenticated user container."""
from __future__ import annotations


class Session:
    def __init__(self) -> None:
        self.user: dict | None = None

    def login(self, user: dict) -> None:
        self.user = user

    def logout(self) -> None:
        self.user = None

    @property
    def user_id(self) -> int | None:
        return int(self.user["id"]) if self.user else None
