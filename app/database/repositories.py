"""Repository functions for user and conversion data."""
from __future__ import annotations

from datetime import date

from app.database.db import Database


class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def count_users(self) -> int:
        row = self.db.fetchone("SELECT COUNT(*) AS c FROM users")
        return int(row["c"] if row else 0)

    def count_admins(self) -> int:
        row = self.db.fetchone("SELECT COUNT(*) AS c FROM users WHERE role='Admin'")
        return int(row["c"] if row else 0)

    def create(self, name: str, email: str, password_hash: str, role: str = "Free") -> int:
        return self.db.execute(
            "INSERT INTO users(name,email,password_hash,role) VALUES(?,?,?,?)",
            (name.strip(), email.lower().strip(), password_hash, role),
        )

    def by_email(self, email: str) -> dict | None:
        return self.db.fetchone("SELECT * FROM users WHERE email=?", (email.lower().strip(),))

    def by_id(self, user_id: int) -> dict | None:
        return self.db.fetchone("SELECT * FROM users WHERE id=?", (user_id,))

    def list_all(self) -> list[dict]:
        return self.db.fetchall(
            """
            SELECT u.id,u.name,u.email,u.role,u.is_active,u.created_at,
                   COUNT(c.id) AS conversion_count
            FROM users u
            LEFT JOIN conversions c ON c.user_id = u.id
            GROUP BY u.id
            ORDER BY u.created_at DESC
            """
        )

    def update_role(self, user_id: int, role: str) -> None:
        self.db.execute(
            "UPDATE users SET role=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (role, user_id),
        )

    def set_active(self, user_id: int, is_active: bool) -> None:
        self.db.execute(
            "UPDATE users SET is_active=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (1 if is_active else 0, user_id),
        )


class ConversionRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, user_id: int, source_path: str, conversion_type: str, output_format: str) -> int:
        return self.db.execute(
            """
            INSERT INTO conversions(user_id,source_path,conversion_type,output_format,status)
            VALUES(?,?,?,?, 'queued')
            """,
            (user_id, source_path, conversion_type, output_format),
        )

    def mark_started(self, conversion_id: int) -> None:
        self.db.execute(
            "UPDATE conversions SET status='running', started_at=CURRENT_TIMESTAMP WHERE id=?",
            (conversion_id,),
        )

    def mark_success(self, conversion_id: int, output_path: str) -> None:
        self.db.execute(
            """
            UPDATE conversions
            SET status='success', output_path=?, finished_at=CURRENT_TIMESTAMP
            WHERE id=?
            """,
            (output_path, conversion_id),
        )

    def mark_error(self, conversion_id: int, error_message: str) -> None:
        self.db.execute(
            """
            UPDATE conversions
            SET status='failed', error_message=?, finished_at=CURRENT_TIMESTAMP
            WHERE id=?
            """,
            (error_message[:1000], conversion_id),
        )

    def list_for_user(self, user_id: int, limit: int = 200) -> list[dict]:
        return self.db.fetchall(
            """
            SELECT * FROM conversions
            WHERE user_id=?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        )

    def list_all(self, limit: int = 500) -> list[dict]:
        return self.db.fetchall(
            """
            SELECT c.*, u.email, u.name
            FROM conversions c
            JOIN users u ON u.id = c.user_id
            ORDER BY c.created_at DESC
            LIMIT ?
            """,
            (limit,),
        )

    def count_today_for_user(self, user_id: int) -> int:
        today = date.today().isoformat()
        row = self.db.fetchone(
            "SELECT COUNT(*) AS c FROM conversions WHERE user_id=? AND DATE(created_at)=DATE(?)",
            (user_id, today),
        )
        return int(row["c"] if row else 0)
