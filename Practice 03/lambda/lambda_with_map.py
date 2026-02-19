# =============================================================
# Using Lambda with map() for Transformation
# =============================================================
# map(function, iterable) applies a function to EVERY item in
# an iterable and returns a map object (convert with list()).
#
# Lambda + map is ideal when you need to transform each element
# of a collection in a concise, readable way.
# =============================================================


# --- Basic transformation: squaring numbers ---
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))

print("Original:", numbers)
print("Squared: ", squared)


# --- String transformation: clean up messy input ---
raw_names = ["  alice ", " BOB", "  Charlie  ", "diana  "]
clean_names = list(map(lambda name: name.strip().title(), raw_names))

print(f"\nRaw:   {raw_names}")
print(f"Clean: {clean_names}")


# --- Numeric transformation: apply a tax rate ---
prices = [10.00, 25.50, 7.99, 42.00, 15.75]
# Add 12% tax to each price
with_tax = list(map(lambda p: round(p * 1.12, 2), prices))

print(f"\nPrices before tax: {prices}")
print(f"Prices after 12%:  {with_tax}")


# --- Transforming data structures: extract fields ---
students = [
    {"name": "Alice", "grade": 92},
    {"name": "Bob", "grade": 85},
    {"name": "Charlie", "grade": 78},
    {"name": "Diana", "grade": 95},
]

# Extract just the names
names = list(map(lambda s: s["name"], students))
print(f"\nStudent names: {names}")

# Create formatted strings from dictionaries
labels = list(map(lambda s: f"{s['name']}: {s['grade']}%", students))
print("Labels:", labels)


# --- map() with multiple iterables ---
# When given multiple iterables, the lambda receives one item
# from each iterable simultaneously
first_names = ["Alice", "Bob", "Charlie"]
last_names = ["Smith", "Jones", "Brown"]

full_names = list(map(lambda f, l: f"{f} {l}", first_names, last_names))
print(f"\nFull names: {full_names}")


# =============================================================
# Practical Application: Student Grade Processor
# =============================================================
# A mini pipeline that transforms raw scores into a report.

raw_scores = [45, 82, 91, 67, 73, 88, 55, 96]

# Step 1: Curve all scores by adding 5 points (max 100)
curved = list(map(lambda s: min(s + 5, 100), raw_scores))

# Step 2: Convert numeric scores to letter grades
to_letter = lambda s: (
    "A" if s >= 90 else
    "B" if s >= 80 else
    "C" if s >= 70 else
    "D" if s >= 60 else "F"
)
letters = list(map(to_letter, curved))

# Step 3: Build a formatted report for each student
report = list(map(
    lambda pair: f"  Score {pair[0]:>2} -> curved {pair[1]:>3} -> {pair[2]}",
    zip(raw_scores, curved, letters)
))

print("\n--- Grade Processing Pipeline ---")
print("  Raw -> Curved -> Letter")
for line in report:
    print(line)
