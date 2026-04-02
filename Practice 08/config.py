"""Database configuration for Practice 08 (PhoneBook + SQL functions/procedures)."""

from __future__ import annotations

import os


def load_config() -> dict[str, str]:
    """Load PostgreSQL connection settings from environment variables."""
    return {
        "dbname": os.getenv("PHONEBOOK_DB_NAME", "phonebook"),
        "user": os.getenv("PHONEBOOK_DB_USER", "postgres"),
        "password": os.getenv("PHONEBOOK_DB_PASSWORD", "NewStrongPassword123"),
        "host": os.getenv("PHONEBOOK_DB_HOST", "localhost"),
        "port": os.getenv("PHONEBOOK_DB_PORT", "5432"),
    }

