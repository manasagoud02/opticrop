import sqlite3
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "opticrop.db"
SQL_PATH = BASE_DIR.parent / "database" / "sample_data.sql"


def ensure_database() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    DATABASE_PATH.touch(exist_ok=True)


@contextmanager
def get_db_connection():
    ensure_database()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    ensure_database()
    with get_db_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                crop_name TEXT NOT NULL,
                score REAL NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS crop_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop_name TEXT UNIQUE NOT NULL,
                n_min REAL NOT NULL,
                n_max REAL NOT NULL,
                p_min REAL NOT NULL,
                p_max REAL NOT NULL,
                k_min REAL NOT NULL,
                k_max REAL NOT NULL,
                temp_min REAL NOT NULL,
                temp_max REAL NOT NULL,
                humidity_min REAL NOT NULL,
                humidity_max REAL NOT NULL,
                ph_min REAL NOT NULL,
                ph_max REAL NOT NULL,
                rainfall_min REAL NOT NULL,
                rainfall_max REAL NOT NULL,
                description TEXT NOT NULL,
                productivity TEXT NOT NULL
            );
            """
        )

        seed_count = conn.execute("SELECT COUNT(*) FROM crop_profiles").fetchone()[0]
        if seed_count == 0 and SQL_PATH.exists():
            conn.executescript(SQL_PATH.read_text(encoding="utf-8"))


def save_recommendation(user_id: int, crop_name: str, score: float, reason: str) -> None:
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO recommendations (user_id, crop_name, score, reason) VALUES (?, ?, ?, ?)",
            (user_id, crop_name, score, reason),
        )


def fetch_user_by_email(email: str):
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()


def fetch_user_by_id(user_id: int):
    with get_db_connection() as conn:
        return conn.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id,)).fetchone()


def create_user(name: str, email: str, password_hash: str) -> int:
    with get_db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        return int(cursor.lastrowid)


def fetch_crop_profiles():
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT crop_name, n_min, n_max, p_min, p_max, k_min, k_max, temp_min, temp_max, humidity_min, humidity_max, ph_min, ph_max, rainfall_min, rainfall_max, description, productivity FROM crop_profiles ORDER BY crop_name"
        ).fetchall()
        return [dict(row) for row in rows]


def fetch_recommendation_history(user_id: int):
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT crop_name, score, reason, created_at FROM recommendations WHERE user_id = ? ORDER BY created_at DESC LIMIT 5",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]


init_db()
