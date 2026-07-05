"""Authentication service using bcrypt hashes."""
from __future__ import annotations

import re

import bcrypt

from app.database.db import Database
from app.database.repositories import UserRepository

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AuthError(Exception):
    pass


class AuthService:
    def __init__(self, db: Database) -> None:
        self.users = UserRepository(db)

    def register(self, name: str, email: str, password: str, force_role: str | None = None) -> dict:
        name = name.strip()
        email = email.lower().strip()
        if len(name) < 2:
            raise AuthError("Name must be at least 2 characters.")
        if not EMAIL_RE.match(email):
            raise AuthError("Invalid email address.")
        if len(password) < 8:
            raise AuthError("Password must be at least 8 characters.")
        if self.users.by_email(email):
            raise AuthError("Email is already registered.")

        role = force_role or ("Admin" if self.users.count_users() == 0 else "Free")
        password_hash = self.hash_password(password)
        user_id = self.users.create(name, email, password_hash, role)
        user = self.users.by_id(user_id)
        assert user is not None
        return user

    def login(self, email: str, password: str) -> dict:
        user = self.users.by_email(email)
        if not user or not self.verify_password(password, user["password_hash"]):
            raise AuthError("Invalid email or password.")
        if not user.get("is_active", 1):
            raise AuthError("This account is disabled.")
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        return self.users.by_email(email)

    @staticmethod
    def hash_password(password: str) -> str:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except Exception:
            return False
