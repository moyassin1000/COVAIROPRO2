import pytest
pytest.importorskip("bcrypt")

from app.auth.auth_service import AuthService
from app.database.db import Database


def test_first_user_is_admin(tmp_path):
    db = Database(tmp_path / "test.sqlite3")
    db.initialize()
    auth = AuthService(db)
    user = auth.register("Admin User", "admin@example.com", "Password123!")
    assert user["role"] == "Admin"
    logged = auth.login("admin@example.com", "Password123!")
    assert logged["email"] == "admin@example.com"
    assert logged["password_hash"] != "Password123!"
