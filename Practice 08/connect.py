"""Connection helpers and DB object initialization for Practice 08."""

from __future__ import annotations

from pathlib import Path

try:
    import psycopg as pg_driver
    from psycopg import Connection
except ModuleNotFoundError as exc:
    raise SystemExit(
        "PostgreSQL driver not found. Install: pip install psycopg[binary]"
    ) from exc

from config import load_config

CREATE_CONTACTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL DEFAULT '',
    phone VARCHAR(32) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

MIGRATE_CONTACTS_SQL = """
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS surname VARCHAR(100) NOT NULL DEFAULT '';

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'contacts_first_name_key'
    ) THEN
        ALTER TABLE contacts DROP CONSTRAINT contacts_first_name_key;
    END IF;
END $$;
"""

CREATE_INDEXES_SQL = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_contacts_name_surname_unique
ON contacts (first_name, surname);

CREATE INDEX IF NOT EXISTS idx_contacts_phone
ON contacts (phone);
"""


def get_connection() -> Connection:
    """Create and return a PostgreSQL connection."""
    return pg_driver.connect(**load_config())


def _execute_sql_file(cur: object, file_path: Path) -> None:
    sql = file_path.read_text(encoding="utf-8").strip()
    if sql:
        cur.execute(sql)


def init_db() -> None:
    """Create table, migrate old schema, and install SQL functions/procedures."""
    base_dir = Path(__file__).resolve().parent
    functions_sql = base_dir / "functions.sql"
    procedures_sql = base_dir / "procedures.sql"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_CONTACTS_TABLE_SQL)
            cur.execute(MIGRATE_CONTACTS_SQL)
            cur.execute(CREATE_INDEXES_SQL)
            _execute_sql_file(cur, functions_sql)
            _execute_sql_file(cur, procedures_sql)
