"""SQLite database wrapper."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Sequence


class Database:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize(self) -> None:
        schema_path = Path(__file__).with_name("schema.sql")
        with self.connect() as conn:
            conn.executescript(schema_path.read_text(encoding="utf-8"))

    def fetchone(self, query: str, params: Sequence | None = None) -> dict | None:
        with self.connect() as conn:
            row = conn.execute(query, params or ()).fetchone()
            return dict(row) if row else None

    def fetchall(self, query: str, params: Sequence | None = None) -> list[dict]:
        with self.connect() as conn:
            rows = conn.execute(query, params or ()).fetchall()
            return [dict(row) for row in rows]

    def execute(self, query: str, params: Sequence | None = None) -> int:
        with self.connect() as conn:
            cur = conn.execute(query, params or ())
            conn.commit()
            return int(cur.lastrowid or 0)

    def executemany(self, query: str, items: Iterable[Sequence]) -> None:
        with self.connect() as conn:
            conn.executemany(query, items)
            conn.commit()
