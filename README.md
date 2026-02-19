# Programming Principles 2

<p align="left">
	<img src="assets/KBTU.avif" alt="University Logo" width="220" />
</p>

PP2 2026 — Spring Semester, Python Snippets

This repository is a collection of Python "practice snippets" that cover the **core Python basics** taught in an **Programming Principles II** course. This course requires us to upload all practice examples/snippet codes that cover the basic topics (aligned with the Python basics learning path on [W3Schools](https://www.w3schools.com/python/)).

## Table of Contents

- [Practice 01 — Python Fundamentals](#practice-01--python-fundamentals)
- [Practice 02 — Control Flow & Logic](#practice-02--control-flow--logic)
- [Practice 03 — Functions & OOP](#practice-03--functions--oop)
- [Repository Structure](#repository-structure)

---

## Practice 01 — Python Fundamentals

> First steps with Python: syntax rules, data types, variables, strings, numbers, casting, and comments.

| # | Topic | Description | Files | Path |
|---|-------|-------------|:-----:|------|
| 1 | **Syntax** | Indentation rules, comments inside code, variable declarations | 4 | [`Practice 01/syntax/`](Practice%2001/syntax/) |
| 2 | **Variables** | Variable assignment, multiple assignment, `type()`, `global` keyword, casting | 5 | [`Practice 01/variables/`](Practice%2001/variables/) |
| 3 | **Data Types** | Overview of Python's built-in data types (str, int, float, list, dict, set, etc.) | 1 | [`Practice 01/data-types/`](Practice%2001/data-types/) |
| 4 | **Numbers** | int, float, complex types, type conversion, random number generation | 5 | [`Practice 01/numbers/`](Practice%2001/numbers/) |
| 5 | **Casting** | Explicit type casting with `int()`, `float()`, `str()` | 3 | [`Practice 01/casting/`](Practice%2001/casting/) |
| 6 | **Strings** | String slicing, splitting, substring checks, escape characters | 4 | [`Practice 01/strings/`](Practice%2001/strings/) |
| 7 | **Comments** | Single-line and multi-line comments, docstring-style comments | 4 | [`Practice 01/comments/`](Practice%2001/comments/) |

---

## Practice 02 — Control Flow & Logic

> Booleans, operators, conditional statements, and loops.

| # | Topic | Description | Files | Path |
|---|-------|-------------|:-----:|------|
| 1 | **Booleans** | Boolean evaluation, truthy/falsy values, `bool()`, `isinstance()`, class `__len__` evaluation | 5 | [`Practice 02/boolean/`](Practice%2002/boolean/) |
| 2 | **Operators** | Comparison, logical, identity, membership, division operators, walrus operator (`:=`) | 6 | [`Practice 02/operators/`](Practice%2002/operators/) |
| 3 | **If-Else** | if/elif/else, match-case (switch), shorthand conditionals, pass statement, grading & temperature classifiers | 7 | [`Practice 02/if-else/`](Practice%2002/if-else/) |
| 4 | **For Loops** | Iterating over sequences, `range()`, nested loops, `break` and `continue` | 5 | [`Practice 02/for-loops/`](Practice%2002/for-loops/) |
| 5 | **While Loops** | While loop basics, `break`, `continue`, while-else pattern | 4 | [`Practice 02/while-loops/`](Practice%2002/while-loops/) |

---

## Practice 03 — Functions & OOP

> Functions, lambda expressions, classes & objects, and inheritance. Each file includes commented practical applications.

| # | Topic | Description | Files | Path |
|---|-------|-------------|:-----:|------|
| 1 | **Functions** | Function definition & docstrings, positional/default/`*args`/`**kwargs` arguments, return values, passing lists and data types | 4 | [`Practice 03/functions/`](Practice%2003/functions/) |
| 2 | **Lambda** | Lambda syntax & basics, lambda with `map()`, `filter()` & `sorted()`, lambda vs regular functions | 4 | [`Practice 03/lambda/`](Practice%2003/lambda/) |
| 3 | **Classes** | Class definition & `__init__`, instance methods & `self`, class vs instance variables, modifying & deleting properties | 4 | [`Practice 03/classes/`](Practice%2003/classes/) |
| 4 | **Inheritance** | Parent/child relationships, `super()` & method overriding, multiple inheritance & MRO, abstract base classes | 4 | [`Practice 03/inheritance/`](Practice%2003/inheritance/) |

---

## How to Run

### Option A: Run a single file

From the repository root:

```bash
python "Practice 01/strings/split.py"
```

### Option B: Run inside VS Code

1. Open a `.py` file.
2. Use **Run Python File** (top-right play button) or the VS Code Run menu.

---

## Repository Structure

```
programming-principles-2/
├── assets/
│   └── KBTU.avif
├── Practice 01/             # Python Fundamentals (28 files)
│   ├── syntax/              #   Indentation, comments, variables
│   ├── variables/           #   Assignment, global, type()
│   ├── data-types/          #   Built-in type overview
│   ├── numbers/             #   int, float, complex, random
│   ├── casting/             #   int(), float(), str()
│   ├── strings/             #   Slicing, splitting, escape chars
│   └── comments/            #   Single-line, multi-line
├── Practice 02/             # Control Flow & Logic (27 files)
│   ├── boolean/             #   bool(), truthy/falsy, isinstance
│   ├── operators/           #   Comparison, logical, walrus
│   ├── if-else/             #   Conditionals, match-case, pass
│   ├── for-loops/           #   Iteration, range, break/continue
│   └── while-loops/         #   While, break, continue, else
├── Practice 03/             # Functions & OOP (16 files)
│   ├── functions/           #   def, args, return, docstrings
│   ├── lambda/              #   Lambda, map, filter, sorted
│   ├── classes/             #   Classes, __init__, self, properties
│   └── inheritance/         #   super(), overriding, ABC
└── README.md
```

## Usage

Educational use.
