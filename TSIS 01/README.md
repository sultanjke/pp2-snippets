# TSIS 01 - Extended PhoneBook (PostgreSQL + Python)

TSIS 01 continues Practice 07 and Practice 08 with a richer PhoneBook schema and more advanced console tools.

## Required structure

- `phonebook.py`
- `config.py`
- `connect.py`
- `functions.sql`
- `procedures.sql`
- `README.md`

## What is implemented

1. Extended contact model:
   - `contacts` now supports `email`, `birthday`, `group_id`.
   - `groups` table for categories (`Family`, `Work`, `Friend`, `Other`).
   - `phones` table for multiple phone numbers per contact (`home/work/mobile`).
2. DB migration safety:
   - old `contacts.phone` values are copied into `phones` as `mobile`.
   - legacy `contacts.phone` column is kept for backward compatibility.
3. New DB-side objects:
   - Function `search_contacts(p_query TEXT)` (matches name, surname, email, phones).
   - Procedure `add_phone(p_contact_name, p_phone, p_type)`.
   - Procedure `move_to_group(p_contact_name, p_group_name)`.
4. Advanced console features:
   - group filtering,
   - partial email search,
   - sorting by `name`, `birthday`, `date_added`,
   - pagination navigation (  `next / prev / quit`).
5. Import/export:
   - export full contacts (with phones + group) to JSON,
   - import from JSON with per-duplicate `skip`/`overwrite`,
   - extended CSV import for `email`, `birthday`, `group`, `phone_type`.

## Setup

Install PostgreSQL driver:

```cmd
python -m pip install psycopg[binary]
```

Set environment variables in Windows CMD:

```cmd
set PHONEBOOK_DB_NAME=phonebook
set PHONEBOOK_DB_USER=phonebook_user
set PHONEBOOK_DB_PASSWORD=YourStrongPassword123
set PHONEBOOK_DB_HOST=localhost
set PHONEBOOK_DB_PORT=5432
```

## Connectivity check + initialization

```cmd
python phonebook.py init
```

This command checks connectivity and installs/updates schema + SQL objects.

## Run interactive menu

```cmd
python phonebook.py
```

Menu options:

```text
TSIS 01 PhoneBook Menu
1. Multi-field search (name/surname/email/phone)
2. Filter by group
3. Search by email (partial)
4. Paginated navigation (next/prev/quit)
5. Add phone to contact (procedure)
6. Move contact to another group (procedure)
7. Export all contacts to JSON
8. Import contacts from JSON
9. Import contacts from CSV (extended)
10. List all contacts with sorting
11. Reinitialize DB objects
0. Exit
```

## CLI examples

Search across name/surname/email/phone:

```cmd
python phonebook.py search --query "gmail"
```

Filter and sort:

```cmd
python phonebook.py list --group "Work" --sort birthday
python phonebook.py list --email "@mail.com" --sort date_added
```

Pagination loop:

```cmd
python phonebook.py page --limit 5
```

Add phone by procedure:

```cmd
python phonebook.py add-phone --contact "Alice Smith" --phone "+77015550199" --type mobile
```

Move to group by procedure:

```cmd
python phonebook.py move-group --contact "Alice Smith" --group "Family"
```

Export JSON:

```cmd
python phonebook.py export-json --file contacts_export.json
```

Import JSON:

```cmd
python phonebook.py import-json --file contacts_export.json
```

Import CSV:

```cmd
python phonebook.py import-csv --file contacts_extended.csv
```

## JSON format (import/export)

```json
[
  {
    "first_name": "Alice",
    "surname": "Smith",
    "email": "alice@gmail.com",
    "birthday": "2001-05-20",
    "group": "Friend",
    "phones": [
      {"phone": "+77015550001", "type": "mobile"},
      {"phone": "+77015550002", "type": "work"}
    ]
  }
]
```

Duplicate contact rule in JSON import:
- duplicate means same normalized `first_name + surname`.
- for each duplicate, app asks: `skip` or `overwrite`.

## CSV format

Recommended CSV headers:

```text
first_name,surname,phone,phone_type,email,birthday,group
```

Rules:
- `birthday` must be `YYYY-MM-DD`.
- `phone_type` must be one of `home`, `work`, `mobile`.
- old CSV (`first_name,phone`) is still accepted.
