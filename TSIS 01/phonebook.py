"""TSIS 01 Extended PhoneBook: richer schema, search, and import/export features."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from connect import get_connection, init_db

PHONE_REGEX = re.compile(r"^\+?[0-9][0-9\-\s]{3,31}$")
VALID_PHONE_TYPES = {"home", "work", "mobile"}
SORT_SQL = {
    "name": "LOWER(c.first_name), LOWER(c.surname), c.id",
    "birthday": "c.birthday NULLS LAST, LOWER(c.first_name), c.id",
    "date_added": "c.created_at, c.id",
}


def normalize_name_value(value: str) -> str:
    return " ".join(value.strip().lower().split())


def clean_name_text(value: str) -> str:
    return " ".join(value.strip().split())


def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone.strip()))


def normalize_phone_type(phone_type: str) -> str:
    value = phone_type.strip().lower()
    if value not in VALID_PHONE_TYPES:
        raise ValueError("Phone type must be home, work, or mobile")
    return value


def parse_iso_birthday(value: str | None) -> date | None:
    if value is None:
        return None

    text = str(value).strip()
    if text == "":
        return None

    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError("Birthday must be in YYYY-MM-DD format") from exc


def ensure_group_id(cur: Any, group_name: str | None) -> int:
    clean_group = (group_name or "Other").strip()
    if clean_group == "":
        clean_group = "Other"

    cur.execute(
        "SELECT id FROM groups WHERE LOWER(name) = LOWER(%s) LIMIT 1;",
        (clean_group,),
    )
    row = cur.fetchone()

    if row:
        return int(row[0])

    cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id;", (clean_group,))
    created = cur.fetchone()
    return int(created[0])


def find_contact_id_by_name_pair(cur: Any, first_name: str, surname: str) -> int | None:
    normalized_first_name = normalize_name_value(first_name)
    normalized_surname = normalize_name_value(surname)

    cur.execute(
        """
        SELECT id
        FROM contacts
        WHERE LOWER(REGEXP_REPLACE(TRIM(first_name), E'\\s+', ' ', 'g')) = %s
          AND LOWER(REGEXP_REPLACE(TRIM(surname), E'\\s+', ' ', 'g')) = %s
        LIMIT 1;
        """,
        (normalized_first_name, normalized_surname),
    )
    row = cur.fetchone()
    if row:
        return int(row[0])
    return None


def add_or_update_phone(cur: Any, contact_id: int, phone: str, phone_type: str) -> None:
    cur.execute(
        """
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
        ON CONFLICT (contact_id, phone)
        DO UPDATE SET type = EXCLUDED.type;
        """,
        (contact_id, phone, phone_type),
    )


def replace_contact_phones(cur: Any, contact_id: int, phones: list[tuple[str, str]]) -> None:
    cur.execute("DELETE FROM phones WHERE contact_id = %s;", (contact_id,))
    for phone, phone_type in phones:
        add_or_update_phone(cur, contact_id, phone, phone_type)


def insert_contact(
    cur: Any,
    first_name: str,
    surname: str,
    email: str | None,
    birthday: date | None,
    group_name: str,
    primary_phone: str,
) -> int:
    group_id = ensure_group_id(cur, group_name)
    cur.execute(
        """
        INSERT INTO contacts(first_name, surname, phone, email, birthday, group_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (first_name, surname, primary_phone, email, birthday, group_id),
    )
    row = cur.fetchone()
    return int(row[0])


def update_contact(
    cur: Any,
    contact_id: int,
    first_name: str,
    surname: str,
    email: str | None,
    birthday: date | None,
    group_name: str,
    primary_phone: str,
) -> None:
    group_id = ensure_group_id(cur, group_name)
    cur.execute(
        """
        UPDATE contacts
        SET first_name = %s,
            surname = %s,
            email = %s,
            birthday = %s,
            group_id = %s,
            phone = %s
        WHERE id = %s;
        """,
        (first_name, surname, email, birthday, group_id, primary_phone, contact_id),
    )


def parse_phones_from_json(item: dict[str, Any]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []

    if isinstance(item.get("phones"), list):
        for phone_item in item["phones"]:
            if isinstance(phone_item, dict):
                raw_phone = str(phone_item.get("phone", "")).strip()
                raw_type = str(phone_item.get("type", "mobile")).strip()
            else:
                raw_phone = str(phone_item).strip()
                raw_type = "mobile"

            if raw_phone == "":
                continue

            if not is_valid_phone(raw_phone):
                raise ValueError(f"Invalid phone format: {raw_phone}")

            clean_type = normalize_phone_type(raw_type)
            result.append((raw_phone, clean_type))

    if not result:
        fallback_phone = str(item.get("phone", "")).strip()
        fallback_type = str(item.get("phone_type", item.get("type", "mobile"))).strip()
        if fallback_phone != "":
            if not is_valid_phone(fallback_phone):
                raise ValueError(f"Invalid phone format: {fallback_phone}")
            result.append((fallback_phone, normalize_phone_type(fallback_type)))

    if not result:
        raise ValueError("At least one phone is required")

    return result


def map_contact_row(row: Any) -> dict[str, Any]:
    return {
        "id": row[0],
        "first_name": row[1],
        "surname": row[2],
        "email": row[3],
        "birthday": row[4],
        "group": row[5],
        "created_at": row[6],
        "phones": row[7],
    }


def print_contacts(rows: list[dict[str, Any]]) -> None:
    if not rows:
        print("No contacts found.")
        return

    print("\nContacts:")
    for index, row in enumerate(rows, start=1):
        full_name = f"{row['first_name']} {row['surname']}".strip()
        email = row.get("email") or "-"

        birthday_value = row.get("birthday")
        if isinstance(birthday_value, date):
            birthday = birthday_value.isoformat()
        elif birthday_value:
            birthday = str(birthday_value)
        else:
            birthday = "-"

        created_value = row.get("created_at")
        if isinstance(created_value, datetime):
            created_at = created_value.strftime("%Y-%m-%d %H:%M")
        elif created_value:
            created_at = str(created_value)
        else:
            created_at = "-"

        phones = row.get("phones") or "-"
        group = row.get("group") or "Other"

        print(
            f"{index}. #{row['id']} {full_name} | email: {email} | "
            f"birthday: {birthday} | group: {group} | phones: {phones} | added: {created_at}"
        )


def search_contacts(query: str) -> list[dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s);", (query,))
            rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "first_name": row[1],
            "surname": row[2],
            "email": row[3],
            "birthday": row[4],
            "group": row[5],
            "phones": row[6],
            "created_at": None,
        }
        for row in rows
    ]


def list_contacts(
    group_name: str | None = None,
    email_part: str | None = None,
    sort_by: str = "name",
) -> list[dict[str, Any]]:
    sort_sql = SORT_SQL.get(sort_by, SORT_SQL["name"])

    where_parts: list[str] = []
    params: list[Any] = []

    if group_name:
        where_parts.append("LOWER(COALESCE(g.name, 'Other')) = LOWER(%s)")
        params.append(group_name)

    if email_part:
        where_parts.append("COALESCE(c.email, '') ILIKE %s")
        params.append(f"%{email_part}%")

    where_sql = ""
    if where_parts:
        where_sql = "WHERE " + " AND ".join(where_parts)

    query = f"""
        SELECT
            c.id,
            c.first_name,
            c.surname,
            COALESCE(c.email, '') AS email,
            c.birthday,
            COALESCE(g.name, 'Other') AS group_name,
            c.created_at,
            COALESCE(STRING_AGG(p.type || ':' || p.phone, ', ' ORDER BY p.id), '') AS phones
        FROM contacts AS c
        LEFT JOIN groups AS g ON g.id = c.group_id
        LEFT JOIN phones AS p ON p.contact_id = c.id
        {where_sql}
        GROUP BY c.id, c.first_name, c.surname, c.email, c.birthday, g.name, c.created_at
        ORDER BY {sort_sql};
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

    return [map_contact_row(row) for row in rows]


def get_paginated_contact_ids(limit: int, offset: int) -> list[int]:
    query = "SELECT * FROM fn_get_contacts_paginated(%s, %s);"

    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(query, (limit, offset))
                rows = cur.fetchall()
                return [int(row[0]) for row in rows]
            except Exception as exc:  # noqa: BLE001 - beginner-friendly fallback
                if "fn_get_contacts_paginated" not in str(exc):
                    raise

                cur.execute(
                    "SELECT id FROM contacts ORDER BY id LIMIT %s OFFSET %s;",
                    (limit, offset),
                )
                rows = cur.fetchall()
                return [int(row[0]) for row in rows]


def get_contacts_by_ids(contact_ids: list[int]) -> list[dict[str, Any]]:
    if not contact_ids:
        return []

    query = """
        SELECT
            c.id,
            c.first_name,
            c.surname,
            COALESCE(c.email, '') AS email,
            c.birthday,
            COALESCE(g.name, 'Other') AS group_name,
            c.created_at,
            COALESCE(STRING_AGG(p.type || ':' || p.phone, ', ' ORDER BY p.id), '') AS phones
        FROM contacts AS c
        LEFT JOIN groups AS g ON g.id = c.group_id
        LEFT JOIN phones AS p ON p.contact_id = c.id
        WHERE c.id = ANY(%s::INT[])
        GROUP BY c.id, c.first_name, c.surname, c.email, c.birthday, g.name, c.created_at
        ORDER BY ARRAY_POSITION(%s::INT[], c.id);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (contact_ids, contact_ids))
            rows = cur.fetchall()

    return [map_contact_row(row) for row in rows]


def get_group_names() -> list[str]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM groups ORDER BY name;")
            rows = cur.fetchall()
    return [str(row[0]) for row in rows]


def call_add_phone(contact_name: str, phone: str, phone_type: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s);", (contact_name, phone, phone_type))


def call_move_to_group(contact_name: str, group_name: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s);", (contact_name, group_name))


def export_contacts_to_json(file_path: Path) -> int:
    query = """
        SELECT
            c.id,
            c.first_name,
            c.surname,
            COALESCE(c.email, '') AS email,
            c.birthday,
            COALESCE(g.name, 'Other') AS group_name,
            c.created_at,
            p.phone,
            p.type
        FROM contacts AS c
        LEFT JOIN groups AS g ON g.id = c.group_id
        LEFT JOIN phones AS p ON p.contact_id = c.id
        ORDER BY c.id, p.id;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    contacts_map: dict[int, dict[str, Any]] = {}

    for row in rows:
        contact_id = int(row[0])

        if contact_id not in contacts_map:
            birthday = row[4].isoformat() if isinstance(row[4], date) else None
            created_at = row[6].isoformat() if isinstance(row[6], datetime) else str(row[6])
            contacts_map[contact_id] = {
                "first_name": row[1],
                "surname": row[2],
                "email": row[3] or "",
                "birthday": birthday,
                "group": row[5] or "Other",
                "created_at": created_at,
                "phones": [],
            }

        if row[7]:
            contacts_map[contact_id]["phones"].append(
                {
                    "phone": row[7],
                    "type": row[8],
                }
            )

    payload = list(contacts_map.values())
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return len(payload)


def ask_duplicate_action(full_name: str) -> str:
    while True:
        choice = input(
            f"Duplicate found for '{full_name}'. Type skip or overwrite: "
        ).strip().lower()
        if choice in {"skip", "overwrite"}:
            return choice
        print("Please type exactly: skip or overwrite")


def import_contacts_from_json(file_path: Path) -> dict[str, int]:
    data = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("JSON root must be a list")

    stats = {"inserted": 0, "updated": 0, "skipped": 0, "invalid": 0}

    with get_connection() as conn:
        with conn.cursor() as cur:
            for index, item in enumerate(data, start=1):
                try:
                    if not isinstance(item, dict):
                        raise ValueError("Each item must be an object")

                    first_name = clean_name_text(str(item.get("first_name", "")))
                    surname = clean_name_text(str(item.get("surname", "")))
                    email = str(item.get("email", "")).strip() or None
                    birthday = parse_iso_birthday(item.get("birthday"))
                    group_name = str(item.get("group", item.get("group_name", "Other"))).strip() or "Other"
                    phones = parse_phones_from_json(item)

                    if first_name == "":
                        raise ValueError("first_name is required")

                    existing_id = find_contact_id_by_name_pair(cur, first_name, surname)
                    full_name = f"{first_name} {surname}".strip()
                    primary_phone = phones[0][0]

                    if existing_id is not None:
                        action = ask_duplicate_action(full_name)
                        if action == "skip":
                            stats["skipped"] += 1
                            continue

                        update_contact(
                            cur,
                            existing_id,
                            first_name,
                            surname,
                            email,
                            birthday,
                            group_name,
                            primary_phone,
                        )
                        replace_contact_phones(cur, existing_id, phones)
                        stats["updated"] += 1
                    else:
                        new_id = insert_contact(
                            cur,
                            first_name,
                            surname,
                            email,
                            birthday,
                            group_name,
                            primary_phone,
                        )
                        replace_contact_phones(cur, new_id, phones)
                        stats["inserted"] += 1

                except Exception as exc:  # noqa: BLE001 - continue import for students
                    print(f"JSON row {index} skipped: {exc}")
                    stats["invalid"] += 1

    return stats


def read_csv_value(row: dict[str, str], names: list[str]) -> str:
    for name in names:
        if name in row and row[name] is not None:
            return str(row[name]).strip()
    return ""


def import_contacts_from_csv(file_path: Path) -> dict[str, int]:
    stats = {"inserted": 0, "updated": 0, "invalid": 0}

    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            raise ValueError("CSV file must include headers")

        with get_connection() as conn:
            with conn.cursor() as cur:
                for line_number, row in enumerate(reader, start=2):
                    try:
                        first_name = read_csv_value(row, ["first_name", "name", "firstname"])
                        surname = read_csv_value(row, ["surname", "last_name", "lastname"])
                        phone = read_csv_value(row, ["phone", "number", "phone_number"])
                        phone_type = read_csv_value(row, ["phone_type", "type"]) or "mobile"
                        email = read_csv_value(row, ["email"])
                        birthday_raw = read_csv_value(row, ["birthday"])
                        group_name = read_csv_value(row, ["group", "category"]) or "Other"

                        first_name = clean_name_text(first_name)
                        surname = clean_name_text(surname)

                        if first_name == "":
                            raise ValueError("first_name is required")
                        if phone == "":
                            raise ValueError("phone is required")
                        if not is_valid_phone(phone):
                            raise ValueError(f"invalid phone: {phone}")

                        clean_type = normalize_phone_type(phone_type)
                        birthday = parse_iso_birthday(birthday_raw)
                        clean_email = email or None

                        existing_id = find_contact_id_by_name_pair(cur, first_name, surname)

                        if existing_id is None:
                            new_id = insert_contact(
                                cur,
                                first_name,
                                surname,
                                clean_email,
                                birthday,
                                group_name,
                                phone,
                            )
                            add_or_update_phone(cur, new_id, phone, clean_type)
                            stats["inserted"] += 1
                        else:
                            update_contact(
                                cur,
                                existing_id,
                                first_name,
                                surname,
                                clean_email,
                                birthday,
                                group_name,
                                phone,
                            )
                            add_or_update_phone(cur, existing_id, phone, clean_type)
                            stats["updated"] += 1

                    except Exception as exc:  # noqa: BLE001 - continue importing next row
                        print(f"CSV row {line_number} skipped: {exc}")
                        stats["invalid"] += 1

    return stats


def choose_sort_option() -> str:
    print("Sort options:")
    print("1. name")
    print("2. birthday")
    print("3. date_added")

    value = input("Choose sort (1/2/3): ").strip()
    if value == "2":
        return "birthday"
    if value == "3":
        return "date_added"
    return "name"


def pagination_loop(limit: int) -> None:
    if limit <= 0:
        raise ValueError("Limit must be greater than 0")

    offset = 0
    while True:
        contact_ids = get_paginated_contact_ids(limit, offset)

        if not contact_ids and offset == 0:
            print("No contacts in database.")
            return

        if not contact_ids:
            print("No more contacts. Showing previous page.")
            offset = max(0, offset - limit)
            continue

        print(f"\nPage (limit={limit}, offset={offset})")
        rows = get_contacts_by_ids(contact_ids)
        print_contacts(rows)

        command = input("Type next / prev / quit: ").strip().lower()
        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command in {"quit", "q", "exit"}:
            break
        else:
            print("Unknown command. Use next, prev, or quit.")


def interactive_menu() -> None:
    while True:
        print("\nTSIS 01 PhoneBook Menu")
        print("1. Multi-field search (name/surname/email/phone)")
        print("2. Filter by group")
        print("3. Search by email (partial)")
        print("4. Paginated navigation (next/prev/quit)")
        print("5. Add phone to contact (procedure)")
        print("6. Move contact to another group (procedure)")
        print("7. Export all contacts to JSON")
        print("8. Import contacts from JSON")
        print("9. Import contacts from CSV (extended)")
        print("10. List all contacts with sorting")
        print("11. Reinitialize DB objects")
        print("0. Exit")

        choice = input("Choose option: ").strip()

        try:
            if choice == "1":
                query = input("Search query: ").strip()
                print_contacts(search_contacts(query))

            elif choice == "2":
                groups = get_group_names()
                if groups:
                    print("Available groups: " + ", ".join(groups))
                group_name = input("Group name: ").strip()
                sort_by = choose_sort_option()
                print_contacts(list_contacts(group_name=group_name, sort_by=sort_by))

            elif choice == "3":
                email_part = input("Email contains: ").strip()
                sort_by = choose_sort_option()
                print_contacts(list_contacts(email_part=email_part, sort_by=sort_by))

            elif choice == "4":
                limit = int(input("Page size (limit): ").strip())
                pagination_loop(limit)

            elif choice == "5":
                contact_name = input("Contact name (first or first surname): ").strip()
                phone = input("New phone: ").strip()
                phone_type = input("Type (home/work/mobile): ").strip()
                call_add_phone(contact_name, phone, phone_type)
                print("Phone added successfully.")

            elif choice == "6":
                contact_name = input("Contact name (first or first surname): ").strip()
                group_name = input("Target group: ").strip()
                call_move_to_group(contact_name, group_name)
                print("Contact moved to group.")

            elif choice == "7":
                file_name = input("JSON output path [contacts_export.json]: ").strip() or "contacts_export.json"
                count = export_contacts_to_json(Path(file_name))
                print(f"Exported contacts: {count}")

            elif choice == "8":
                file_name = input("JSON input path: ").strip()
                if file_name == "":
                    print("Path cannot be empty.")
                    continue
                stats = import_contacts_from_json(Path(file_name))
                print(
                    f"JSON import done. inserted={stats['inserted']}, "
                    f"updated={stats['updated']}, skipped={stats['skipped']}, invalid={stats['invalid']}"
                )

            elif choice == "9":
                file_name = input("CSV input path: ").strip()
                if file_name == "":
                    print("Path cannot be empty.")
                    continue
                stats = import_contacts_from_csv(Path(file_name))
                print(
                    f"CSV import done. inserted={stats['inserted']}, "
                    f"updated={stats['updated']}, invalid={stats['invalid']}"
                )

            elif choice == "10":
                sort_by = choose_sort_option()
                print_contacts(list_contacts(sort_by=sort_by))

            elif choice == "11":
                init_db()
                print("DB objects reinitialized.")

            elif choice == "0":
                print("Goodbye.")
                break

            else:
                print("Invalid option.")

        except ValueError as exc:
            print(f"Input error: {exc}")
        except Exception as exc:  # noqa: BLE001 - beginner readable error output
            print(f"Database error: {exc}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TSIS 01 Extended PhoneBook")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Create/extend schema and install SQL objects.")
    subparsers.add_parser("menu", help="Run interactive menu.")

    search_parser = subparsers.add_parser("search", help="Multi-field search using DB function.")
    search_parser.add_argument("--query", required=True, help="Part of name/surname/email/phone.")

    list_parser = subparsers.add_parser("list", help="List contacts with optional filters.")
    list_parser.add_argument("--group", help="Filter by group name.")
    list_parser.add_argument("--email", help="Filter by email contains.")
    list_parser.add_argument(
        "--sort",
        choices=["name", "birthday", "date_added"],
        default="name",
        help="Sort order.",
    )

    page_parser = subparsers.add_parser("page", help="Run pagination loop (next/prev/quit).")
    page_parser.add_argument("--limit", type=int, default=5, help="Page size.")

    add_phone_parser = subparsers.add_parser("add-phone", help="Add phone using procedure.")
    add_phone_parser.add_argument("--contact", required=True, help="Contact name.")
    add_phone_parser.add_argument("--phone", required=True, help="Phone number.")
    add_phone_parser.add_argument(
        "--type",
        required=True,
        choices=["home", "work", "mobile"],
        help="Phone type.",
    )

    move_group_parser = subparsers.add_parser("move-group", help="Move contact to group.")
    move_group_parser.add_argument("--contact", required=True, help="Contact name.")
    move_group_parser.add_argument("--group", required=True, help="Target group name.")

    export_parser = subparsers.add_parser("export-json", help="Export all contacts to JSON.")
    export_parser.add_argument("--file", required=True, help="Output JSON file path.")

    import_json_parser = subparsers.add_parser("import-json", help="Import contacts from JSON.")
    import_json_parser.add_argument("--file", required=True, help="Input JSON file path.")

    import_csv_parser = subparsers.add_parser("import-csv", help="Import contacts from CSV.")
    import_csv_parser.add_argument("--file", required=True, help="Input CSV file path.")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    init_db()

    try:
        if args.command == "init":
            print("TSIS 01 schema and SQL objects are ready.")

        elif args.command == "search":
            print_contacts(search_contacts(args.query))

        elif args.command == "list":
            rows = list_contacts(group_name=args.group, email_part=args.email, sort_by=args.sort)
            print_contacts(rows)

        elif args.command == "page":
            pagination_loop(args.limit)

        elif args.command == "add-phone":
            call_add_phone(args.contact, args.phone, args.type)
            print("Phone added successfully.")

        elif args.command == "move-group":
            call_move_to_group(args.contact, args.group)
            print("Contact moved to group.")

        elif args.command == "export-json":
            count = export_contacts_to_json(Path(args.file))
            print(f"Exported contacts: {count}")

        elif args.command == "import-json":
            stats = import_contacts_from_json(Path(args.file))
            print(
                f"JSON import done. inserted={stats['inserted']}, "
                f"updated={stats['updated']}, skipped={stats['skipped']}, invalid={stats['invalid']}"
            )

        elif args.command == "import-csv":
            stats = import_contacts_from_csv(Path(args.file))
            print(
                f"CSV import done. inserted={stats['inserted']}, "
                f"updated={stats['updated']}, invalid={stats['invalid']}"
            )

        else:
            interactive_menu()

    except Exception as exc:  # noqa: BLE001 - final friendly message
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
