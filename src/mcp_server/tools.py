"""
Core DB helper functions used by MCP tools.
"""

from typing import Any, Dict, Optional, List
import sqlite3
from datetime import datetime


def open_db(db_path: str) -> sqlite3.Connection:
    """
    Open a SQLite connection and configure rows as dict-like objects.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_customer(db_path: str, id: int) -> Dict[str, Any]:
    """Return one customer by ID."""
    conn = open_db(db_path)
    row = conn.execute("SELECT * FROM customers WHERE id = ?", (id,)).fetchone()
    conn.close()
    if row is None:
        return {"status": "not_found", "customer": None}
    return {"status": "ok", "customer": dict(row)}


def list_customers(
    db_path: str,
    status: Optional[str] = None,
    limit: int = 20,
) -> Dict[str, Any]:
    """Return a list of customers, optionally filtered by status."""
    conn = open_db(db_path)
    if status:
        rows = conn.execute(
            "SELECT * FROM customers WHERE status = ? LIMIT ?",
            (status, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM customers LIMIT ?",
            (limit,),
        ).fetchall()
    conn.close()
    return {"status": "ok", "customers": [dict(r) for r in rows]}


def update_customer(
    db_path: str,
    id: int,
    fields: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Update selected fields on a customer record.

    Allowed keys: email, phone, status, name.
    """
    allowed = {"email", "phone", "status", "name"}
    updates = [f"{k} = ?" for k in fields if k in allowed]
    values: List[Any] = [fields[k] for k in fields if k in allowed]

    if not updates:
        return {"status": "error", "message": "No valid fields to update."}

    conn = open_db(db_path)
    conn.execute(
        f"UPDATE customers SET {', '.join(updates)}, updated_at = ? WHERE id = ?",
        (*values, datetime.utcnow().isoformat(), id),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM customers WHERE id = ?", (id,)).fetchone()
    conn.close()

    if row is None:
        return {"status": "not_found", "customer": None}
    return {"status": "ok", "customer": dict(row)}


def create_ticket(
    db_path: str,
    id: int,
    issue: str,
    priority: str = "medium",
) -> Dict[str, Any]:
    """Create a new ticket for the given customer."""
    created_at = datetime.utcnow().isoformat()
    conn = open_db(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO tickets (customer_id, issue, status, priority, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (id, issue, "open", priority, created_at),
    )
    ticket_id = cur.lastrowid
    conn.commit()
    conn.close()

    return {
        "status": "ok",
        "ticket": {
            "id": ticket_id,
            "customer_id": id,
            "issue": issue,
            "status": "open",
            "priority": priority,
            "created_at": created_at,
        },
    }


def get_customer_history(db_path: str, id: int) -> Dict[str, Any]:
    """Return all tickets associated with the given customer."""
    conn = open_db(db_path)
    rows = conn.execute(
        "SELECT * FROM tickets WHERE customer_id = ? ORDER BY created_at DESC",
        (id,),
    ).fetchall()
    conn.close()
    return {"status": "ok", "tickets": [dict(r) for r in rows]}