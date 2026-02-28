"""
Smiling Critters — Database Layer
SQLite via Python's built-in sqlite3.
Stores: chat messages, session metadata, safety flags, parent alerts.
"""

import sqlite3
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


DB_PATH = os.getenv("DB_PATH", str(Path(__file__).parent.parent / "data" / "smiling_critters.db"))


def _get_conn() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            critter_id  TEXT    NOT NULL,
            started_at  TEXT    NOT NULL,
            ended_at    TEXT,
            duration_s  INTEGER,
            message_count INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  INTEGER NOT NULL REFERENCES sessions(id),
            role        TEXT    NOT NULL,  -- 'user' or 'assistant'
            content     TEXT    NOT NULL,
            critter_id  TEXT,
            timestamp   TEXT    NOT NULL,
            flagged     INTEGER DEFAULT 0  -- 0=safe, 1=redirect, 2=alert, 3=crisis
        );

        CREATE TABLE IF NOT EXISTS safety_flags (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  INTEGER REFERENCES sessions(id),
            message_id  INTEGER REFERENCES messages(id),
            flag_level  TEXT    NOT NULL,
            reason      TEXT,
            note        TEXT,
            timestamp   TEXT    NOT NULL,
            acknowledged INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS settings (
            key         TEXT PRIMARY KEY,
            value       TEXT
        );
    """)
    conn.commit()

    # Insert defaults if not present
    defaults = {
        "parent_pin":        "1234",
        "daily_limit_min":   "45",
        "reminder_30":       "1",
        "reminder_60":       "1",
        "quiet_hours_start": "20:00",
        "quiet_hours_end":   "07:00",
        "child_name":        "Friend",
        "llm_prefer_local":  "1",
        # AI config — defaults to env vars; overridable in parent dashboard
        "ollama_url":        os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "ollama_model":      os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
        "gemini_key":        os.getenv("GEMINI_API_KEY", ""),
    }
    for k, v in defaults.items():
        conn.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v)
        )
    conn.commit()
    conn.close()


# ─── Sessions ────────────────────────────────────────────────────────────────

def start_session(critter_id: str) -> int:
    conn = _get_conn()
    cur = conn.execute(
        "INSERT INTO sessions (critter_id, started_at) VALUES (?, ?)",
        (critter_id, datetime.now().isoformat())
    )
    session_id = cur.lastrowid
    conn.commit()
    conn.close()
    return session_id


def end_session(session_id: int, duration_s: int, message_count: int):
    conn = _get_conn()
    conn.execute(
        """UPDATE sessions
           SET ended_at=?, duration_s=?, message_count=?
           WHERE id=?""",
        (datetime.now().isoformat(), duration_s, message_count, session_id)
    )
    conn.commit()
    conn.close()


def get_recent_sessions(limit: int = 20) -> List[Dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM sessions ORDER BY started_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Messages ────────────────────────────────────────────────────────────────

def save_message(
    session_id: int,
    role: str,
    content: str,
    critter_id: str,
    flagged: int = 0
) -> int:
    conn = _get_conn()
    cur = conn.execute(
        """INSERT INTO messages (session_id, role, content, critter_id, timestamp, flagged)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (session_id, role, content, critter_id, datetime.now().isoformat(), flagged)
    )
    msg_id = cur.lastrowid
    conn.commit()
    conn.close()
    return msg_id


def get_session_messages(session_id: int) -> List[Dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM messages WHERE session_id=? ORDER BY timestamp ASC",
        (session_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Safety flags ─────────────────────────────────────────────────────────────

def save_flag(
    session_id: int,
    message_id: int,
    flag_level: str,
    reason: str,
    note: str
):
    conn = _get_conn()
    conn.execute(
        """INSERT INTO safety_flags
           (session_id, message_id, flag_level, reason, note, timestamp)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (session_id, message_id, flag_level, reason, note, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_unacknowledged_flags() -> List[Dict]:
    conn = _get_conn()
    rows = conn.execute(
        """SELECT f.*, m.content as message_content
           FROM safety_flags f
           LEFT JOIN messages m ON f.message_id = m.id
           WHERE f.acknowledged = 0
           ORDER BY f.timestamp DESC"""
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def acknowledge_flag(flag_id: int):
    conn = _get_conn()
    conn.execute("UPDATE safety_flags SET acknowledged=1 WHERE id=?", (flag_id,))
    conn.commit()
    conn.close()


def get_all_flags(limit: int = 50) -> List[Dict]:
    conn = _get_conn()
    rows = conn.execute(
        """SELECT f.*, m.content as message_content
           FROM safety_flags f
           LEFT JOIN messages m ON f.message_id = m.id
           ORDER BY f.timestamp DESC LIMIT ?""", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Settings ────────────────────────────────────────────────────────────────

def get_setting(key: str, default: Optional[str] = None) -> Optional[str]:
    conn = _get_conn()
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_setting(key: str, value: str):
    conn = _get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value))
    )
    conn.commit()
    conn.close()


def get_all_settings() -> dict:
    conn = _get_conn()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    return {r["key"]: r["value"] for r in rows}


# ─── Analytics ───────────────────────────────────────────────────────────────

def get_usage_stats() -> dict:
    conn = _get_conn()

    total_sessions = conn.execute("SELECT COUNT(*) as n FROM sessions").fetchone()["n"]
    total_messages = conn.execute("SELECT COUNT(*) as n FROM messages WHERE role='user'").fetchone()["n"]
    total_flags    = conn.execute("SELECT COUNT(*) as n FROM safety_flags").fetchone()["n"]
    unread_flags   = conn.execute("SELECT COUNT(*) as n FROM safety_flags WHERE acknowledged=0").fetchone()["n"]

    critter_usage = conn.execute(
        "SELECT critter_id, COUNT(*) as n FROM sessions GROUP BY critter_id ORDER BY n DESC"
    ).fetchall()

    recent_duration = conn.execute(
        "SELECT AVG(duration_s) as avg FROM sessions WHERE duration_s IS NOT NULL"
    ).fetchone()["avg"] or 0

    conn.close()
    return {
        "total_sessions": total_sessions,
        "total_messages": total_messages,
        "total_flags": total_flags,
        "unread_flags": unread_flags,
        "critter_usage": [dict(r) for r in critter_usage],
        "avg_session_min": round(recent_duration / 60, 1),
    }
