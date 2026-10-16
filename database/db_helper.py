import os
import sqlite3
from contextlib import closing
from pathlib import Path

from .schema import APP_NAME, AUTH_METHODS, SCHEMA_FEATURES


class DatabaseHelper:
    def __init__(self, db_path=None):
        app_slug = "".join(
            character.lower() if character.isalnum() else "_"
            for character in APP_NAME
        ).strip("_") or "generated_app"
        default_path = Path.home() / ".generated_app" / app_slug / "app.sqlite3"
        self.db_path = Path(
            db_path or os.environ.get("APP_DATABASE_PATH", str(default_path))
        )
        if str(self.db_path) != ":memory:":
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.create_tables()

    def get_connection(self):
        connection = sqlite3.connect(str(self.db_path))
        connection.row_factory = sqlite3.Row
        return connection

    def create_tables(self):
        with closing(self.get_connection()) as connection, connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS app_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            if "Arayüz: Ana sayfa kartları" in SCHEMA_FEATURES:
                connection.execute("""
                    CREATE TABLE IF NOT EXISTS content_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL DEFAULT '',
                        position INTEGER NOT NULL DEFAULT 0,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            if "Login Sistemi" in SCHEMA_FEATURES:
                connection.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT UNIQUE,
                        password_salt BLOB,
                        password_hash BLOB,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        CHECK (username IS NOT NULL OR email IS NOT NULL)
                    )
                """)
                if "email" in AUTH_METHODS:
                    connection.execute("""
                        CREATE TABLE IF NOT EXISTS verification_codes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL,
                            code_hash BLOB NOT NULL,
                            expires_at TEXT NOT NULL,
                            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
            oauth_methods = tuple(
                method for method in AUTH_METHODS
                if method not in ("username", "email")
            )
            if oauth_methods:
                connection.execute("""
                    CREATE TABLE IF NOT EXISTS oauth_accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        provider TEXT NOT NULL,
                        provider_user_id TEXT NOT NULL,
                        user_id INTEGER,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(provider, provider_user_id),
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )
                """)

    def add_record(self, record_type, payload):
        with closing(self.get_connection()) as connection, connection:
            cursor = connection.execute(
                "INSERT INTO app_records (record_type, payload) VALUES (?, ?)",
                (record_type, payload),
            )
            return cursor.lastrowid

    def get_records(self, record_type=None):
        with closing(self.get_connection()) as connection, connection:
            if record_type is None:
                rows = connection.execute(
                    "SELECT * FROM app_records ORDER BY id"
                ).fetchall()
            else:
                rows = connection.execute(
                    "SELECT * FROM app_records WHERE record_type = ? ORDER BY id",
                    (record_type,),
                ).fetchall()
            return [dict(row) for row in rows]
