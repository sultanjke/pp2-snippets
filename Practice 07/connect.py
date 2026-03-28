"""PostgreSQL connection helpers and schema initialization."""

from __future__ import annotations

try:
    import psycopg as pg_driver
    from psycopg import Connection as connection
except ModuleNotFoundError as exc:
    raise SystemExit(
        "PostgreSQL driver not found. Install: pip install psycopg[binary]"
    ) from exc

from config import load_config

CREATE_CONTACTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(32) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_NAME_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_contacts_lower_name
ON contacts ((LOWER(first_name)));
"""

CREATE_PHONE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_contacts_phone
ON contacts (phone);
"""


def get_connection() -> connection:
    """Create and return a PostgreSQL connection."""
    return pg_driver.connect(**load_config())


def init_db() -> None:
    """Create the PhoneBook schema if it does not exist."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_CONTACTS_TABLE_SQL)
            cur.execute(CREATE_NAME_INDEX_SQL)
            cur.execute(CREATE_PHONE_INDEX_SQL)
