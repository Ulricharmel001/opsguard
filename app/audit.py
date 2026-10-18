import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).parent / "audit.db"


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_conn()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL NOT NULL,
                request TEXT NOT NULL,
                tool TEXT NOT NULL,
                args_json TEXT NOT NULL,
                environment TEXT NOT NULL,
                hard_rule TEXT,
                decider_choice TEXT,
                confidence REAL,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                human_response TEXT,
                explanation TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def log_decision(
    request: str,
    tool: str,
    args: Dict[str, Any],
    environment: str,
    hard_rule: Optional[str],
    decider_choice: Optional[str],
    confidence: Optional[float],
    action: str,
    status: str = "pending",
    human_response: Optional[str] = None,
    explanation: Optional[str] = None,
):
    import time

    conn = _get_conn()
    try:
        conn.execute(
            """
            INSERT INTO decisions (ts, request, tool, args_json, environment,
                                   hard_rule, decider_choice, confidence, action,
                                   status, human_response, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                time.time(),
                request,
                tool,
                json.dumps(args),
                environment,
                hard_rule,
                decider_choice,
                confidence,
                action,
                status,
                human_response,
                explanation,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def list_decisions(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    conn = _get_conn()
    try:
        cur = conn.execute(
            """
            SELECT id, ts, request, tool, args_json, environment,
                   hard_rule, decider_choice, confidence, action,
                   status, human_response, explanation
            FROM decisions
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        rows = cur.fetchall()
        res = []
        for r in rows:
            d = dict(r)
            try:
                d["args"] = json.loads(d.pop("args_json"))
            except Exception:
                d["args"] = {}
            res.append(d)
        return res
    finally:
        conn.close()
