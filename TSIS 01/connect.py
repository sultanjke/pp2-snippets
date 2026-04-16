"""Connection helpers and DB initialization for TSIS 01 Extended PhoneBook."""

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

CREATE_BASE_CONTACTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL DEFAULT '',
    phone VARCHAR(32) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_GROUPS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
"""

SEED_DEFAULT_GROUPS_SQL = """
INSERT INTO groups(name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;
"""

MIGRATE_CONTACTS_SQL = """
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS surname VARCHAR(100) NOT NULL DEFAULT '';
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS phone VARCHAR(32);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email VARCHAR(100);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER;

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

CREATE_CONTACTS_FOREIGN_KEY_SQL = """
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'contacts_group_fk'
    ) THEN
        ALTER TABLE contacts
        ADD CONSTRAINT contacts_group_fk
        FOREIGN KEY (group_id)
        REFERENCES groups(id);
    END IF;
END $$;

UPDATE contacts AS c
SET group_id = g.id
FROM groups AS g
WHERE c.group_id IS NULL
  AND g.name = 'Other';
"""

CREATE_PHONES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile'))
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'phones_contact_phone_unique'
    ) THEN
        ALTER TABLE phones
        ADD CONSTRAINT phones_contact_phone_unique UNIQUE(contact_id, phone);
    END IF;
END $$;
"""

CREATE_INDEXES_SQL = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_contacts_name_surname_unique
ON contacts (first_name, surname);

CREATE INDEX IF NOT EXISTS idx_contacts_phone
ON contacts (phone);

CREATE INDEX IF NOT EXISTS idx_contacts_group_id
ON contacts (group_id);

CREATE INDEX IF NOT EXISTS idx_contacts_email
ON contacts (email);

CREATE INDEX IF NOT EXISTS idx_phones_phone
ON phones (phone);

CREATE INDEX IF NOT EXISTS idx_phones_contact_id
ON phones (contact_id);
"""

MIGRATE_OLD_PHONE_TO_PHONES_SQL = """
INSERT INTO phones (contact_id, phone, type)
SELECT c.id, c.phone, 'mobile'
FROM contacts AS c
WHERE c.phone IS NOT NULL
  AND TRIM(c.phone) <> ''
ON CONFLICT (contact_id, phone) DO NOTHING;
"""


def get_connection() -> Connection:
    """Create and return a PostgreSQL connection."""
    return pg_driver.connect(**load_config())


def _execute_sql_file(cur: object, file_path: Path) -> None:
    sql = file_path.read_text(encoding="utf-8").strip()
    if sql:
        cur.execute(sql)


def init_db() -> None:
    """Create/extend schema and install SQL functions/procedures."""
    base_dir = Path(__file__).resolve().parent
    functions_sql = base_dir / "functions.sql"
    procedures_sql = base_dir / "procedures.sql"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_BASE_CONTACTS_TABLE_SQL)
            cur.execute(CREATE_GROUPS_TABLE_SQL)
            cur.execute(SEED_DEFAULT_GROUPS_SQL)
            cur.execute(MIGRATE_CONTACTS_SQL)
            cur.execute(CREATE_CONTACTS_FOREIGN_KEY_SQL)
            cur.execute(CREATE_PHONES_TABLE_SQL)
            cur.execute(CREATE_INDEXES_SQL)
            cur.execute(MIGRATE_OLD_PHONE_TO_PHONES_SQL)
            _execute_sql_file(cur, functions_sql)
            _execute_sql_file(cur, procedures_sql)
