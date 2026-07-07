import sqlite3
import hashlib
import datetime
import config


def _connect():
    return sqlite3.connect(config.CACHE_DB)


def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS llm_cache (
                key TEXT PRIMARY KEY,
                service TEXT,
                user_id INTEGER,
                prompt TEXT,
                response TEXT,
                created_at TEXT
            )
        """)


def make_key(service: str, user_id: int, prompt: str) -> str:
    raw = f"{service}|{user_id}|{prompt}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def get(key: str):
    with _connect() as conn:
        row = conn.execute(
            "SELECT response FROM llm_cache WHERE key = ?", (key,)
        ).fetchone()
    return row[0] if row else None


def put(key: str, service: str, user_id: int, prompt: str, response: str):
    created_at = datetime.datetime.now().isoformat(timespec="seconds")
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO llm_cache "
            "(key, service, user_id, prompt, response, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (key, service, user_id, prompt, response, created_at),
        )
