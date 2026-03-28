"""PhoneBook practical exercise (PostgreSQL + Python)."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Any

try:
    from psycopg import IntegrityError
except ModuleNotFoundError:
    class IntegrityError(Exception):
        """Fallback error type when PostgreSQL driver is missing."""

        pass

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from connect import get_connection, init_db

PHONE_PATTERN = re.compile(r"^[+]?[0-9][0-9\-\s]{3,31}$")


def normalize_name(value: str) -> str:
    name = value.strip()
    if not name:
        raise ValueError("Name cannot be empty.")
    return name


def normalize_phone(value: str) -> str:
    phone = " ".join(value.strip().split())
    if not PHONE_PATTERN.fullmatch(phone):
        raise ValueError("Phone must contain digits and may include '+' '-' spaces.")
    return phone


def insert_contact(first_name: str, phone: str) -> bool:
    first_name = normalize_name(first_name)
    phone = normalize_phone(phone)
    query = """
    INSERT INTO contacts (first_name, phone)
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (first_name, phone))
            return cur.rowcount == 1


def _extract_name_and_phone(row: dict[str, str]) -> tuple[str, str] | None:
    lower_row = {key.lower().strip(): (value or "").strip() for key, value in row.items() if key}
    name = (
        lower_row.get("first_name")
        or lower_row.get("name")
        or lower_row.get("username")
        or lower_row.get("user_name")
    )
    phone = lower_row.get("phone") or lower_row.get("phone_number") or lower_row.get("number")

    if not name or not phone:
        return None
    return name, phone


def insert_from_csv(csv_path: str) -> dict[str, int]:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file does not exist: {path}")

    inserted = 0
    skipped = 0
    invalid = 0

    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV file must include a header row.")

        for row in reader:
            extracted = _extract_name_and_phone(row)
            if extracted is None:
                invalid += 1
                continue

            name, phone = extracted
            try:
                if insert_contact(name, phone):
                    inserted += 1
                else:
                    skipped += 1
            except ValueError:
                invalid += 1

    return {"inserted": inserted, "skipped": skipped, "invalid": invalid}


def update_contact(current_name: str, new_name: str | None, new_phone: str | None) -> bool:
    current_name = normalize_name(current_name)
    fields: list[str] = []
    values: list[str] = []

    if new_name:
        fields.append("first_name = %s")
        values.append(normalize_name(new_name))
    if new_phone:
        fields.append("phone = %s")
        values.append(normalize_phone(new_phone))

    if not fields:
        raise ValueError("Provide new_name and/or new_phone for update.")

    values.append(current_name)
    query = f"""
    UPDATE contacts
    SET {", ".join(fields)}
    WHERE first_name = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            return cur.rowcount == 1


def query_contacts(name: str | None = None, phone_prefix: str | None = None) -> list[dict[str, Any]]:
    where_clauses: list[str] = []
    params: list[str] = []

    if name:
        where_clauses.append("LOWER(first_name) LIKE LOWER(%s)")
        params.append(f"%{name.strip()}%")

    if phone_prefix:
        where_clauses.append("phone LIKE %s")
        params.append(f"{phone_prefix.strip()}%")

    where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    query = f"""
    SELECT first_name, phone
    FROM contacts
    {where_sql}
    ORDER BY first_name;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

    return [{"first_name": row[0], "phone": row[1]} for row in rows]


def delete_contact(name: str | None = None, phone: str | None = None) -> bool:
    if not name and not phone:
        raise ValueError("Provide either name or phone to delete a contact.")

    if name:
        query = "DELETE FROM contacts WHERE first_name = %s;"
        params = (normalize_name(name),)
    else:
        query = "DELETE FROM contacts WHERE phone = %s;"
        params = (normalize_phone(phone or ""),)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.rowcount == 1


def print_contacts(rows: list[dict[str, Any]]) -> None:
    if not rows:
        print("No contacts found.")
        return

    print("\nContacts:")
    for index, row in enumerate(rows, start=1):
        print(f"{index}. {row['first_name']} - {row['phone']}")


def prompt_insert_console() -> None:
    first_name = input("Enter first name: ").strip()
    phone = input("Enter phone: ").strip()
    inserted = insert_contact(first_name, phone)
    if inserted:
        print("Contact inserted.")
    else:
        print("Contact already exists (same name or phone).")


def prompt_update() -> None:
    current_name = input("Current first name: ").strip()
    new_name = input("New first name (leave empty to keep): ").strip() or None
    new_phone = input("New phone (leave empty to keep): ").strip() or None
    updated = update_contact(current_name, new_name, new_phone)
    print("Contact updated." if updated else "Contact not found.")


def prompt_query() -> None:
    name = input("Filter by name (optional): ").strip() or None
    phone_prefix = input("Filter by phone prefix (optional): ").strip() or None
    print_contacts(query_contacts(name=name, phone_prefix=phone_prefix))


def prompt_delete() -> None:
    mode = input("Delete by [n]ame or [p]hone? ").strip().lower()
    if mode == "n":
        name = input("First name: ").strip()
        deleted = delete_contact(name=name)
    elif mode == "p":
        phone = input("Phone: ").strip()
        deleted = delete_contact(phone=phone)
    else:
        print("Invalid option.")
        return
    print("Contact deleted." if deleted else "Contact not found.")


def interactive_menu() -> None:
    while True:
        print("\nPhoneBook Menu")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Show all contacts")
        print("0. Exit")
        choice = input("Choose option: ").strip()

        try:
            if choice == "1":
                csv_path = input("CSV file path: ").strip()
                result = insert_from_csv(csv_path)
                print(
                    f"Import complete. Inserted={result['inserted']}, "
                    f"Skipped={result['skipped']}, Invalid={result['invalid']}"
                )
            elif choice == "2":
                prompt_insert_console()
            elif choice == "3":
                prompt_update()
            elif choice == "4":
                prompt_query()
            elif choice == "5":
                prompt_delete()
            elif choice == "6":
                print_contacts(query_contacts())
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid menu option.")
        except FileNotFoundError as exc:
            print(exc)
        except ValueError as exc:
            print(f"Input error: {exc}")
        except IntegrityError as exc:
            print(f"Database constraint error: {exc}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PhoneBook exercise (PostgreSQL + Python)")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Create PhoneBook table and indexes.")

    import_parser = subparsers.add_parser("import-csv", help="Insert contacts from CSV file.")
    import_parser.add_argument("--file", required=True, help="Path to CSV file.")

    add_parser = subparsers.add_parser("add", help="Insert one contact.")
    add_parser.add_argument("--name", required=True, help="First name.")
    add_parser.add_argument("--phone", required=True, help="Phone number.")

    update_parser = subparsers.add_parser("update", help="Update contact name or phone.")
    update_parser.add_argument("--name", required=True, help="Current first name.")
    update_parser.add_argument("--new-name", help="New first name.")
    update_parser.add_argument("--new-phone", help="New phone.")

    query_parser = subparsers.add_parser("find", help="Query contacts by filters.")
    query_parser.add_argument("--name", help="Name filter (contains match).")
    query_parser.add_argument("--phone-prefix", help="Phone prefix filter.")

    delete_parser = subparsers.add_parser("delete", help="Delete by name or phone.")
    delete_group = delete_parser.add_mutually_exclusive_group(required=True)
    delete_group.add_argument("--name", help="First name.")
    delete_group.add_argument("--phone", help="Phone.")

    subparsers.add_parser("list", help="Show all contacts.")
    subparsers.add_parser("menu", help="Run interactive console menu.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    init_db()

    try:
        if args.command == "init":
            print("PhoneBook table is ready.")
        elif args.command == "import-csv":
            result = insert_from_csv(args.file)
            print(
                f"Import complete. Inserted={result['inserted']}, "
                f"Skipped={result['skipped']}, Invalid={result['invalid']}"
            )
        elif args.command == "add":
            if insert_contact(args.name, args.phone):
                print("Contact inserted.")
            else:
                print("Contact already exists (same name or phone).")
        elif args.command == "update":
            updated = update_contact(args.name, args.new_name, args.new_phone)
            print("Contact updated." if updated else "Contact not found.")
        elif args.command == "find":
            print_contacts(query_contacts(name=args.name, phone_prefix=args.phone_prefix))
        elif args.command == "delete":
            deleted = delete_contact(name=args.name, phone=args.phone)
            print("Contact deleted." if deleted else "Contact not found.")
        elif args.command == "list":
            print_contacts(query_contacts())
        else:
            interactive_menu()
    except FileNotFoundError as exc:
        print(exc)
    except ValueError as exc:
        print(f"Input error: {exc}")
    except IntegrityError as exc:
        print(f"Database constraint error: {exc}")


if __name__ == "__main__":
    main()
