# Practice 08 - PhoneBook with Functions & Procedures

This practice continues `Practice 07` and uses the same PostgreSQL database (`phonebook`).

## Required structure

- `phonebook.py`
- `config.py`
- `connect.py`
- `functions.sql`
- `procedures.sql`
- `README.md`

## What is implemented

1. Function `fn_search_contacts(pattern)`:
   returns rows that match part of `first_name`, `surname`, or `phone`.
2. Procedure `sp_upsert_user(...)`:
   inserts a new user, or updates phone if user already exists.
3. Procedure `sp_insert_many_users(...)`:
   accepts arrays of names/surnames/phones, uses `FOR` loop and `IF`,
   validates phone format, and returns invalid rows via `INOUT`.
4. Function `fn_get_contacts_paginated(limit, offset)`:
   returns paginated contacts with `LIMIT/OFFSET`.
5. Procedure `sp_delete_user(...)`:
   deletes by username (`first_name`) or phone and returns deleted count.

## Setup

Install driver:

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

Run:

```cmd
python phonebook.py init
```

If this succeeds, table migrations and SQL functions/procedures were installed correctly.

## Run interactive menu

```cmd
python phonebook.py
```

Menu:

```text
PhoneBook Menu (Practice 08)
1. Search contacts by pattern
2. Upsert one user (procedure)
3. Insert many users (procedure + loop + IF)
4. Paginated list (function)
5. Delete by username or phone (procedure)
6. Reinitialize SQL functions/procedures
0. Exit
```

## CLI examples

Search:

```cmd
python phonebook.py search --pattern "ali"
```

Upsert one user:

```cmd
python phonebook.py upsert --first-name "Alice" --surname "Smith" --phone "+77015550101"
```

Bulk insert/update:

```cmd
python phonebook.py bulk --user "Bob,Stone,+77015550102" --user "Eve,Ray,INVALID_PHONE"
```

Pagination:

```cmd
python phonebook.py page --limit 5 --offset 0
```

Delete by username:

```cmd
python phonebook.py delete --username "Alice"
```

Delete by phone:

```cmd
python phonebook.py delete --phone "+77015550101"
```

