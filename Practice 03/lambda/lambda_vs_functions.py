# =============================================================
# Anonymous Functions (Lambda) vs Regular Functions (def)
# =============================================================
# This example compares both approaches side by side so you
# can see the trade-offs and know when to pick each one.
# =============================================================


# --- 1. Side-by-side: same logic, two styles ---

# Regular function
def square_def(x):
    """Return the square of x."""
    return x * x

# Equivalent lambda
square_lambda = lambda x: x * x

# Both produce the same result
print("def square:   ", square_def(7))
print("lambda square:", square_lambda(7))


# --- 2. Name and identity ---
# Regular functions have a proper __name__; lambdas show '<lambda>'
print(f"\ndef __name__:    '{square_def.__name__}'")
print(f"lambda __name__: '{square_lambda.__name__}'")


# --- 3. Docstrings ---
# Only regular functions support docstrings for documentation
print(f"\ndef __doc__:    '{square_def.__doc__}'")
print(f"lambda __doc__: {square_lambda.__doc__}")  # None


# --- 4. Complexity: lambdas are limited to one expression ---
# Regular functions can use loops, assignments, and multiple lines.

# Regular function — clear and readable for complex logic
def analyze_number(n):
    """Classify a number and return a detailed description."""
    properties = []
    if n > 0:
        properties.append("positive")
    elif n < 0:
        properties.append("negative")
    else:
        properties.append("zero")

    if n != 0 and n % 2 == 0:
        properties.append("even")
    elif n != 0:
        properties.append("odd")

    return f"{n} is {', '.join(properties)}"

# Lambda — forced to use chained ternaries, much harder to read
analyze_lambda = lambda n: f"{n} is " + (
    "zero" if n == 0
    else ("positive, even" if n > 0 and n % 2 == 0
    else ("positive, odd" if n > 0
    else ("negative, even" if n % 2 == 0
    else "negative, odd")))
)

print("\n--- Complex logic comparison ---")
test_values = [10, -3, 0, 7, -8]
for val in test_values:
    print(f"  def:    {analyze_number(val)}")
    print(f"  lambda: {analyze_lambda(val)}")
    print()


# --- 5. Where lambdas WIN: concise inline usage ---
# Lambdas are ideal when passed directly to functions like
# sorted(), map(), and filter() — no need for a named function.

data = [{"name": "Alice", "gpa": 3.8}, {"name": "Bob", "gpa": 3.5}, {"name": "Charlie", "gpa": 3.9}]

# Lambda: short and fits naturally inside sorted()
ranked = sorted(data, key=lambda s: s["gpa"], reverse=True)

print("--- Lambda shines as an inline key ---")
for s in ranked:
    print(f"  {s['name']}: {s['gpa']}")


# --- 6. Where def WINS: reusable, documented, debuggable ---
def format_student(student):
    """Format a student record into a readable report line."""
    gpa = student["gpa"]
    status = "Honor Roll" if gpa >= 3.7 else "Good Standing"
    return f"{student['name']} (GPA: {gpa}) — {status}"

# Clear, self-documenting, easy to debug
print("\n--- def shines for reusable logic ---")
for s in data:
    print(f"  {format_student(s)}")


# =============================================================
# Practical Application: Choosing the Right Tool
# =============================================================
# A real scenario showing lambda and def working TOGETHER.

orders = [
    {"customer": "Alice",   "total": 150.00, "items": 3},
    {"customer": "Bob",     "total": 45.00,  "items": 1},
    {"customer": "Charlie", "total": 230.00, "items": 5},
    {"customer": "Diana",   "total": 89.00,  "items": 2},
    {"customer": "Eve",     "total": 310.00, "items": 7},
]

# USE LAMBDA: simple inline filter + sort
#   These are one-liners that don't need names or docs
big_orders = sorted(
    filter(lambda o: o["total"] > 100, orders),
    key=lambda o: o["total"],
    reverse=True
)

# USE DEF: the formatting logic is complex and reusable
def format_order(order):
    """Format an order into a printable receipt line."""
    avg = order["total"] / order["items"]
    tier = "Premium" if order["total"] >= 200 else "Standard"
    return (
        f"  {order['customer']:<10} | "
        f"${order['total']:>6.2f} | "
        f"{order['items']} items | "
        f"avg ${avg:.2f}/item | "
        f"{tier}"
    )

print("\n--- Orders over $100 (lambda filters & sorts, def formats) ---")
print(f"  {'Customer':<10} | {'Total':>7} | Items  | Avg/Item    | Tier")
print(f"  {'-' * 58}")
for o in big_orders:
    print(format_order(o))

# =============================================================
# Summary:
#   Lambda — best for short, throwaway, inline operations
#   def    — best for complex, reusable, documented logic
#   In practice, use BOTH together for clean, readable code.
# =============================================================
