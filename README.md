# Programming Principles 2

<p align="left">
  <img src="assets/KBTU.avif" alt="University Logo" width="220" />
</p>

PP2 2026 - Spring Semester, Python Snippets

This repository collects Python practice snippets and practical exercises for Programming Principles II, aligned with the Python basics learning path on [W3Schools](https://www.w3schools.com/python/).

## Table of Contents

- [Practice 01 - Python Fundamentals](#practice-01---python-fundamentals)
- [Practice 02 - Control Flow and Logic](#practice-02---control-flow-and-logic)
- [Practice 03 - Functions and OOP](#practice-03---functions-and-oop)
- [Practice 04 - Iterators and Generators](#practice-04---iterators-and-generators)
- [Practice 05 - Regular Expressions](#practice-05---regular-expressions)
- [Practice 06 - File Handling and Built-in Functions](#practice-06---file-handling-and-built-in-functions)
- [Practice 07 - PhoneBook (PostgreSQL + Python)](#practice-07---phonebook-postgresql--python)
- [Practice 08 - PhoneBook with Functions and Procedures](#practice-08---phonebook-with-functions-and-procedures)
- [How to Run](#how-to-run)
- [Repository Structure](#repository-structure)

---

## Practice 01 - Python Fundamentals

> First steps with Python: syntax, data types, variables, strings, numbers, casting, and comments.

| # | Topic | Description | Files | Path |
|---|-------|-------------|:-----:|------|
| 1 | **Syntax** | Indentation rules, comments, variable declarations | 4 | [`Practice 01/syntax/`](Practice%2001/syntax/) |
| 2 | **Variables** | Assignment, multiple assignment, `type()`, `global`, casting | 5 | [`Practice 01/variables/`](Practice%2001/variables/) |
| 3 | **Data Types** | Overview of Python built-in data types | 1 | [`Practice 01/data-types/`](Practice%2001/data-types/) |
| 4 | **Numbers** | `int`, `float`, `complex`, conversion, random numbers | 5 | [`Practice 01/numbers/`](Practice%2001/numbers/) |
| 5 | **Casting** | Explicit conversions with `int()`, `float()`, `str()` | 3 | [`Practice 01/casting/`](Practice%2001/casting/) |
| 6 | **Strings** | Slicing, split, substring checks, escape chars | 4 | [`Practice 01/strings/`](Practice%2001/strings/) |
| 7 | **Comments** | Single-line and multi-line comments | 4 | [`Practice 01/comments/`](Practice%2001/comments/) |

---

## Practice 02 - Control Flow and Logic

> Booleans, operators, conditional statements, and loops.

| # | Topic | Description | Files | Path |
|---|-------|-------------|:-----:|------|
| 1 | **Booleans** | Truthy/falsy, `bool()`, `isinstance()`, class evaluation | 5 | [`Practice 02/boolean/`](Practice%2002/boolean/) |
| 2 | **Operators** | Comparison, logical, identity, membership, walrus operator | 6 | [`Practice 02/operators/`](Practice%2002/operators/) |
| 3 | **If-Else** | `if/elif/else`, `match`, shorthand conditions, examples | 7 | [`Practice 02/if-else/`](Practice%2002/if-else/) |
| 4 | **For Loops** | Iteration, `range()`, nested loops, `break`/`continue` | 5 | [`Practice 02/for-loops/`](Practice%2002/for-loops/) |
| 5 | **While Loops** | `while`, `break`, `continue`, `while-else` | 4 | [`Practice 02/while-loops/`](Practice%2002/while-loops/) |

---

## Practice 03 - Functions and OOP

> Functions, lambda expressions, classes, objects, and inheritance.

| # | Topic | Description | Files | Path |
|---|-------|-------------|:-----:|------|
| 1 | **Functions** | Definition, arguments, return values, passing data types | 4 | [`Practice 03/functions/`](Practice%2003/functions/) |
| 2 | **Lambda** | Lambda basics, `map()`, `filter()`, `sorted()` | 4 | [`Practice 03/lambda/`](Practice%2003/lambda/) |
| 3 | **Classes** | Class basics, `__init__`, methods, class vs instance vars | 4 | [`Practice 03/classes/`](Practice%2003/classes/) |
| 4 | **Inheritance** | Parent/child, overriding, multiple inheritance, abstracts | 4 | [`Practice 03/inheritance/`](Practice%2003/inheritance/) |

---

## Practice 04 - Iterators and Generators

> Iteration patterns plus dates, math, and JSON exercises.

| # | Topic | Description | Files | Path |
|---|-------|-------------|:-----:|------|
| 1 | **Iterators and Generators** | `iter()`, `next()`, custom iterators, `yield`, generator expressions | 4 | [`Practice 04/iterators-and-generators/`](Practice%2004/iterators-and-generators/) |
| 2 | **Dates and Times** | `datetime`, formatting, time differences, timezones | 4 | [`Practice 04/dates-and-times/`](Practice%2004/dates-and-times/) |
| 3 | **Math** | Built-in math, `math` module, `random` module | 3 | [`Practice 04/math/`](Practice%2004/math/) |
| 4 | **JSON** | Parse, serialize, read/write JSON files | 4 | [`Practice 04/json/`](Practice%2004/json/) |

---

## Practice 05 - Regular Expressions

> Pattern matching and text processing with Python `re`.

| # | Topic | Description | Files | Path |
|---|-------|-------------|:-----:|------|
| 1 | **RegEx** | `search`, `match`, `findall`, `split`, `sub`, flags, validators | 4 | [`Practice 05/regex/`](Practice%2005/regex/) |

---

## Practice 06 - File Handling and Built-in Functions

> Working with files, directories, and data-processing helpers.

| # | Topic | Description | Files | Path |
|---|-------|-------------|:-----:|------|
| 1 | **File Handling** | File modes, reading/writing, append, copy/delete with `shutil` | 3 | [`Practice 06/file_handling/`](Practice%2006/file_handling/) |
| 2 | **Directory Management** | Create/list/change/remove directories, move files | 2 | [`Practice 06/directory_management/`](Practice%2006/directory_management/) |
| 3 | **Built-in Functions** | `map`, `filter`, `reduce`, `enumerate`, `zip`, sorting and conversions | 2 | [`Practice 06/builtin_functions/`](Practice%2006/builtin_functions/) |

---

## Practice 07 - PhoneBook (PostgreSQL + Python)

> Practical exercise with PostgreSQL integration in Python.

| # | Topic | Description | Path |
|---|-------|-------------|------|
| 1 | **PhoneBook CRUD** | Table design, CSV import, console insert, update, filter queries, delete by name/phone | [`Practice 07/`](Practice%2007/) |

---

## Practice 08 - PhoneBook with Functions and Procedures

> Continuation of Practice 07 using PostgreSQL functions and stored procedures.

| # | Topic | Description | Path |
|---|-------|-------------|------|
| 1 | **SQL Functions and Procedures** | Pattern search function, upsert procedure, bulk insert procedure with validation, pagination function, delete procedure | [`Practice 08/`](Practice%2008/) |

---

## How to Run

Run a single file:

```bash
python "Practice 01/strings/split.py"
```

Run Practice 07 PhoneBook:

```bash
python "Practice 07/phonebook.py" init
python "Practice 07/phonebook.py"
```

Run Practice 08 PhoneBook:

```bash
python "Practice 08/phonebook.py" init
python "Practice 08/phonebook.py"
```

---

## Repository Structure

```text
pp2-snippets/
|-- assets/
|   `-- KBTU.avif
|-- Practice 01/
|   |-- syntax/
|   |-- variables/
|   |-- data-types/
|   |-- numbers/
|   |-- casting/
|   |-- strings/
|   |-- comments/
|   |-- getting-started/
|   |-- home/
|   `-- README.md
|-- Practice 02/
|   |-- boolean/
|   |-- operators/
|   |-- if-else/
|   |-- for-loops/
|   |-- while-loops/
|   `-- README.md
|-- Practice 03/
|   |-- functions/
|   |-- lambda/
|   |-- classes/
|   |-- inheritance/
|   |-- defense.py
|   `-- README.md
|-- Practice 04/
|   |-- iterators-and-generators/
|   |-- dates-and-times/
|   |-- math/
|   |-- json/
|   |-- exercises/
|   |   |-- date.py
|   |   |-- generators.py
|   |   |-- math.py
|   |   `-- json/
|   |-- defense/
|   `-- README.md
|-- Practice 05/
|   |-- regex/
|   |-- raw.txt
|   |-- receipt_parser.py
|   `-- README.md
|-- Practice 06/
|   |-- file_handling/
|   |-- directory_management/
|   |-- builtin_functions/
|   |-- defense/
|   `-- README.md
|-- Practice 07/
|   |-- README.md
|   |-- phonebook.py
|   |-- connect.py
|   |-- config.py
|   |-- contacts.csv
|   `-- requirements.txt
|-- Practice 08/
|   |-- README.md
|   |-- phonebook.py
|   |-- connect.py
|   |-- config.py
|   |-- functions.sql
|   `-- procedures.sql
`-- README.md
```

## Usage

Educational use.
