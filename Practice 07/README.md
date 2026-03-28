# Practice 07 - PhoneBook (PostgreSQL + Python)

## Features

- Table design for `contacts`
- Insert contacts from CSV
- Insert contacts from console
- Update contact first name or phone
- Query contacts with filters (name contains, phone prefix)
- Delete contacts by name or phone

## Database schema

```sql
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(32) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Indexes are also created for faster name and phone search.

## Requirements

- PostgreSQL server running locally (default `localhost:5432`)
- Python package: `psycopg` (v3 binary)

Install Python dependency:

```cmd
python -m pip install -r "Practice 07\requirements.txt"
```

## Create database in pgAdmin

1. Open pgAdmin and connect to your PostgreSQL server.
2. Right-click `Databases` -> `Create` -> `Database...`
3. Create database named `phonebook`.
4. Optional: create a dedicated user (`phonebook_user`) in `Login/Group Roles`.
5. In Query Tool, run:

```sql
ALTER ROLE phonebook_user WITH LOGIN PASSWORD 'YourStrongPassword123';
GRANT CONNECT ON DATABASE phonebook TO phonebook_user;
```

Then switch Query Tool to database `phonebook` and run:

```sql
GRANT USAGE, CREATE ON SCHEMA public TO phonebook_user;
```

## Configure environment variables (Windows CMD)

From `Practice 07` folder:

```cmd
set PHONEBOOK_DB_NAME=phonebook
set PHONEBOOK_DB_USER=phonebook_user
set PHONEBOOK_DB_PASSWORD=YourStrongPassword123
set PHONEBOOK_DB_HOST=localhost
set PHONEBOOK_DB_PORT=5432
```

If you use the default superuser, replace `PHONEBOOK_DB_USER` with `postgres` and set its real password.

## Run

Check PostgreSQL connectivity and initialize table:

```cmd
python phonebook.py init
```

If this succeeds, the app connected to PostgreSQL correctly and prints `PhoneBook table is ready.`

Run interactive menu:

```cmd
python phonebook.py
```

## Interactive menu options

After running `python phonebook.py`, you get:

```text
PhoneBook Menu
1. Insert from CSV
2. Insert from console
3. Update contact
4. Query contacts
5. Delete contact
6. Show all contacts
0. Exit
```

## Useful CLI commands

Import from CSV:

```cmd
python phonebook.py import-csv --file "contacts.csv"
```

Insert one contact:

```cmd
python phonebook.py add --name "Diana" --phone "+77019990000"
```

Update contact:

```cmd
python phonebook.py update --name "Diana" --new-phone "+77018887766"
```

Find contacts:

```cmd
python phonebook.py find --name "di" --phone-prefix "+7701"
```

Delete contact:

```cmd
python phonebook.py delete --name "Diana"
```

List all contacts:

```cmd
python phonebook.py list
```

## Common issues

- `role "phonebook_user" is not permitted to log in`:
  Run `ALTER ROLE phonebook_user WITH LOGIN PASSWORD '...'`.
- `password authentication failed`:
  Check `PHONEBOOK_DB_USER` and `PHONEBOOK_DB_PASSWORD`.
- `PostgreSQL driver not found`:
  Run `python -m pip install -r requirements.txt` in the same interpreter environment.
