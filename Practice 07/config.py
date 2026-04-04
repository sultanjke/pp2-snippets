"""Database configuration for the PhoneBook exercise."""

from __future__ import annotations

import os


def load_config() -> dict[str, str]:
    """Return PostgreSQL connection settings from environment variables."""
    return {
        "dbname": os.getenv("PHONEBOOK_DB_NAME", "phonebook"),
        "user": os.getenv("PHONEBOOK_DB_USER", "postgres"),
        "password": os.getenv("PHONEBOOK_DB_PASSWORD", "NewStrongPassword123"),
        "host": os.getenv("PHONEBOOK_DB_HOST", "localhost"),
        "port": os.getenv("PHONEBOOK_DB_PORT", "5432"),
    }
