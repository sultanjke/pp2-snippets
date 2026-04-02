"""Practice 08 PhoneBook: PostgreSQL functions and stored procedures."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from connect import get_connection, init_db


def search_contacts(pattern: str) -> list[dict[str, Any]]:
    query = "SELECT * FROM fn_search_contacts(%s);"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (pattern,))
            rows = cur.fetchall()
    return [
        {
            "id": row[0],
            "first_name": row[1],
            "surname": row[2],
            "phone": row[3],
        }
        for row in rows
    ]


def get_contacts_paginated(limit: int, offset: int) -> list[dict[str, Any]]:
    query = "SELECT * FROM fn_get_contacts_paginated(%s, %s);"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit, offset))
            rows = cur.fetchall()
    return [
        {
            "id": row[0],
            "first_name": row[1],
            "surname": row[2],
            "phone": row[3],
        }
        for row in rows
    ]


def upsert_user(first_name: str, surname: str, phone: str) -> None:
    query = "CALL sp_upsert_user(%s, %s, %s);"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (first_name, surname, phone))


def insert_many_users(users: list[tuple[str, str, str]]) -> list[str]:
    first_names = [user[0] for user in users]
    surnames = [user[1] for user in users]
    phones = [user[2] for user in users]

    query = "CALL sp_insert_many_users(%s, %s, %s, %s);"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (first_names, surnames, phones, []))
            row = cur.fetchone()

    if row and row[0]:
        return list(row[0])
    return []


def delete_user(username: str | None = None, phone: str | None = None) -> int:
    query = "CALL sp_delete_user(%s, %s, %s);"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (username, phone, 0))
            row = cur.fetchone()

    if row:
        return int(row[0])
    return 0


def print_contacts(rows: list[dict[str, Any]]) -> None:
    if not rows:
        print("No contacts found.")
        return

    print("\nContacts:")
    for index, row in enumerate(rows, start=1):
        full_name = f"{row['first_name']} {row['surname']}".strip()
        print(f"{index}. #{row['id']} {full_name} - {row['phone']}")


def prompt_bulk_users() -> list[tuple[str, str, str]]:
    count = int(input("How many users to add/update? ").strip())
    users: list[tuple[str, str, str]] = []
    for idx in range(1, count + 1):
        print(f"\nUser {idx}:")
        first_name = input("First name: ").strip()
        surname = input("Surname (optional): ").strip()
        phone = input("Phone: ").strip()
        users.append((first_name, surname, phone))
    return users


def interactive_menu() -> None:
    while True:
        print("\nPhoneBook Menu (Practice 08)")
        print("1. Search contacts by pattern")
        print("2. Upsert one user (procedure)")
        print("3. Insert many users (procedure + loop + IF)")
        print("4. Paginated list (function)")
        print("5. Delete by username or phone (procedure)")
        print("6. Reinitialize SQL functions/procedures")
        print("0. Exit")
        choice = input("Choose option: ").strip()

        try:
            if choice == "1":
                pattern = input("Pattern: ").strip()
                print_contacts(search_contacts(pattern))
            elif choice == "2":
                first_name = input("First name: ").strip()
                surname = input("Surname (optional): ").strip()
                phone = input("Phone: ").strip()
                upsert_user(first_name, surname, phone)
                print("User inserted/updated.")
            elif choice == "3":
                users = prompt_bulk_users()
                invalid = insert_many_users(users)
                if invalid:
                    print("Invalid rows:")
                    for item in invalid:
                        print(f"- {item}")
                else:
                    print("All users processed successfully.")
            elif choice == "4":
                limit = int(input("LIMIT: ").strip())
                offset = int(input("OFFSET: ").strip())
                print_contacts(get_contacts_paginated(limit, offset))
            elif choice == "5":
                username = input("Username (press Enter to skip): ").strip() or None
                phone = input("Phone (press Enter to skip): ").strip() or None
                deleted_count = delete_user(username=username, phone=phone)
                print(f"Deleted rows: {deleted_count}")
            elif choice == "6":
                init_db()
                print("Functions/procedures reinitialized.")
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")
        except ValueError as exc:
            print(f"Input error: {exc}")
        except Exception as exc:  # noqa: BLE001 - clear console message for students
            print(f"Database error: {exc}")


def parse_user_items(items: list[str]) -> list[tuple[str, str, str]]:
    users: list[tuple[str, str, str]] = []
    for raw in items:
        parts = [part.strip() for part in raw.split(",")]
        if len(parts) != 3:
            raise ValueError("Each --user must look like: first_name,surname,phone")
        users.append((parts[0], parts[1], parts[2]))
    return users


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Practice 08 PhoneBook")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Create/migrate table and install SQL functions/procedures.")

    search_parser = subparsers.add_parser("search", help="Search by pattern using SQL function.")
    search_parser.add_argument("--pattern", required=True, help="Part of name, surname, or phone.")

    upsert_parser = subparsers.add_parser("upsert", help="Insert/update one user using SQL procedure.")
    upsert_parser.add_argument("--first-name", required=True, help="First name.")
    upsert_parser.add_argument("--surname", default="", help="Surname.")
    upsert_parser.add_argument("--phone", required=True, help="Phone number.")

    bulk_parser = subparsers.add_parser("bulk", help="Bulk insert/update using SQL procedure.")
    bulk_parser.add_argument(
        "--user",
        action="append",
        required=True,
        help="User as first_name,surname,phone (repeat --user for many rows).",
    )

    page_parser = subparsers.add_parser("page", help="Get paginated rows using SQL function.")
    page_parser.add_argument("--limit", required=True, type=int, help="LIMIT value.")
    page_parser.add_argument("--offset", required=True, type=int, help="OFFSET value.")

    delete_parser = subparsers.add_parser("delete", help="Delete by username or phone using procedure.")
    delete_parser.add_argument("--username", help="Username (first_name).")
    delete_parser.add_argument("--phone", help="Phone number.")

    subparsers.add_parser("menu", help="Run interactive menu.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    init_db()

    try:
        if args.command == "init":
            print("Practice 08 SQL objects are ready.")
        elif args.command == "search":
            print_contacts(search_contacts(args.pattern))
        elif args.command == "upsert":
            upsert_user(args.first_name, args.surname, args.phone)
            print("User inserted/updated.")
        elif args.command == "bulk":
            users = parse_user_items(args.user)
            invalid = insert_many_users(users)
            if invalid:
                print("Invalid rows:")
                for item in invalid:
                    print(f"- {item}")
            else:
                print("All users processed successfully.")
        elif args.command == "page":
            print_contacts(get_contacts_paginated(args.limit, args.offset))
        elif args.command == "delete":
            deleted_count = delete_user(args.username, args.phone)
            print(f"Deleted rows: {deleted_count}")
        else:
            interactive_menu()
    except Exception as exc:  # noqa: BLE001 - clear console message for students
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()

