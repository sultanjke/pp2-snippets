# =============================================================
# Using Lambda with filter() and sorted()
# =============================================================
# filter(function, iterable) — keeps items where the function
#   returns True; discards the rest.
#
# sorted(iterable, key=function) — returns a new sorted list;
#   the key function determines the comparison value.
#
# Both pair naturally with lambdas for concise, readable code.
# =============================================================


# ===================== FILTER ================================

# --- Basic filtering: keep even numbers ---
numbers = [3, 12, 7, 18, 5, 22, 9, 14]
evens = list(filter(lambda x: x % 2 == 0, numbers))

print("All numbers:", numbers)
print("Even only:  ", evens)


# --- Filter strings by length ---
words = ["hi", "python", "is", "a", "powerful", "language", "ok"]
long_words = list(filter(lambda w: len(w) > 3, words))

print(f"\nAll words:           {words}")
print(f"Longer than 3 chars: {long_words}")


# --- Filter dictionaries by a condition ---
products = [
    {"name": "Laptop",   "price": 999, "in_stock": True},
    {"name": "Mouse",    "price": 25,  "in_stock": False},
    {"name": "Keyboard", "price": 75,  "in_stock": True},
    {"name": "Monitor",  "price": 300, "in_stock": False},
    {"name": "Headset",  "price": 60,  "in_stock": True},
]

# Keep only products that are in stock AND under $100
affordable_available = list(filter(
    lambda p: p["in_stock"] and p["price"] < 100,
    products
))

print("\n--- Affordable & in-stock products ---")
for p in affordable_available:
    print(f"  {p['name']}: ${p['price']}")


# ===================== SORTED ================================

# --- Sort numbers in descending order ---
scores = [78, 92, 85, 67, 95, 88]
desc_scores = sorted(scores, key=lambda x: -x)

print(f"\nOriginal scores:  {scores}")
print(f"Descending order: {desc_scores}")


# --- Sort strings by last character ---
names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
by_last_char = sorted(names, key=lambda name: name[-1])

print(f"\nNames sorted by last character: {by_last_char}")


# --- Sort tuples by a specific element ---
# Sort (name, age) pairs by age
people = [("Alice", 30), ("Bob", 22), ("Charlie", 27), ("Diana", 25)]
by_age = sorted(people, key=lambda person: person[1])

print(f"\nPeople sorted by age:")
for name, age in by_age:
    print(f"  {name}, {age}")


# --- Sort dictionaries by a computed value ---
students = [
    {"name": "Alice",   "grades": [90, 88, 95]},
    {"name": "Bob",     "grades": [70, 82, 75]},
    {"name": "Charlie", "grades": [85, 91, 88]},
    {"name": "Diana",   "grades": [92, 96, 89]},
]

# Sort by average grade (highest first)
by_avg = sorted(
    students,
    key=lambda s: sum(s["grades"]) / len(s["grades"]),
    reverse=True
)

print("\n--- Students ranked by average grade ---")
for s in by_avg:
    avg = sum(s["grades"]) / len(s["grades"])
    print(f"  {s['name']}: avg = {avg:.1f}")


# =============================================================
# Practical Application: E-Commerce Product Search
# =============================================================
# Combine filter + sorted to build a simple product search
# that narrows results and orders them by relevance.

catalog = [
    {"name": "Python Crash Course",       "category": "book",    "price": 29.99, "rating": 4.7},
    {"name": "Wireless Mouse",            "category": "tech",    "price": 19.99, "rating": 4.3},
    {"name": "Mechanical Keyboard",       "category": "tech",    "price": 89.99, "rating": 4.8},
    {"name": "Clean Code",                "category": "book",    "price": 34.99, "rating": 4.5},
    {"name": "USB-C Hub",                 "category": "tech",    "price": 35.00, "rating": 4.1},
    {"name": "Automate the Boring Stuff", "category": "book",    "price": 25.99, "rating": 4.6},
    {"name": "Monitor Stand",             "category": "tech",    "price": 45.00, "rating": 3.9},
]

# Step 1: FILTER — keep only tech products under $50
filtered = list(filter(
    lambda p: p["category"] == "tech" and p["price"] < 50,
    catalog
))

# Step 2: SORT — order results by rating (best first)
results = sorted(filtered, key=lambda p: p["rating"], reverse=True)

print("\n--- Search: Tech products under $50, best rated first ---")
for item in results:
    print(f"  {item['rating']}★  ${item['price']:<6.2f}  {item['name']}")
