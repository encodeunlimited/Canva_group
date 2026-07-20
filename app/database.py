"""
Database module for Canva Monitor V2.
Manages the SQLite database for storing current and historical Canva URLs/tokens.
"""
import sqlite3
from typing import Optional, Tuple
from datetime import datetime

from config.config import DATABASE_PATH
from app.logger import logger

def get_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with row factory configured."""
    conn = sqlite3.connect(DATABASE_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initializes the database schema if it doesn't exist."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS current_link (
                    id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    token TEXT NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    token TEXT NOT NULL,
                    detected_at TIMESTAMP NOT NULL
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def get_current() -> Optional[Tuple[str, str]]:
    """
    Retrieves the current known URL and token.
    Returns a tuple of (url, token) or None if empty.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url, token FROM current_link WHERE id = 1")
            row = cursor.fetchone()
            if row:
                return row['url'], row['token']
            return None
    except sqlite3.Error as e:
        logger.error(f"Failed to get current link from database: {e}")
        raise

def save_current(url: str, token: str) -> None:
    """Saves the current known URL and token."""
    now = datetime.now()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO current_link (id, url, token, updated_at) 
                VALUES (1, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET 
                    url=excluded.url, 
                    token=excluded.token, 
                    updated_at=excluded.updated_at
            """, (url, token, now))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to save current link to database: {e}")
        raise

def add_history(url: str, token: str) -> None:
    """Adds a new record to the history table."""
    now = datetime.now()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO history (url, token, detected_at) 
                VALUES (?, ?, ?)
            """, (url, token, now))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to add history record: {e}")
        raise

init_db()
