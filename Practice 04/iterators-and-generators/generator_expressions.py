# =============================================================
# Generator Expressions
# =============================================================

# A generator expression looks like a list comprehension
# but uses parentheses () instead of brackets [].
# It produces values lazily — one at a time, without
# building the full list in memory.


# List comprehension (builds entire list in memory)
squares_list = [x ** 2 for x in range(6)]

# Generator expression (produces values on demand)
squares_gen = (x ** 2 for x in range(6))

print("List:", squares_list)
print("Generator object:", squares_gen)

print("\n--- Consuming the generator ---")
for square in squares_gen:
    print(f"  {square}", end="")
print()


# Generator expressions work directly inside functions
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

total = sum(x ** 2 for x in numbers)
largest = max(x * 3 for x in numbers)
smallest = min(abs(x) for x in [-5, 3, -1, 7, -9])

print(f"\nsum of squares:  {total}")
print(f"max of tripled:  {largest}")
print(f"min of absolute: {smallest}")


# Filtering with a condition inside the expression
words = ["apple", "banana", "avocado", "cherry", "apricot", "blueberry"]

a_words = list(word.upper() for word in words if word.startswith("a"))
print(f"\nWords starting with 'a' (uppercased): {a_words}")


# Memory comparison: generator vs list
import sys

list_version = [x for x in range(10_000)]
gen_version = (x for x in range(10_000))

print(f"\n--- Memory usage ---")
print(f"  List (10k items): {sys.getsizeof(list_version):,} bytes")
print(f"  Generator:        {sys.getsizeof(gen_version):,} bytes")


# Chaining generator expressions
raw_prices = ["  $12.50 ", "$8.99", " $25.00  ", "$3.75", "  $15.20"]

# Pipeline: strip -> remove $ -> convert to float -> filter above $10
cleaned = (price.strip() for price in raw_prices)
numeric = (float(price.replace("$", "")) for price in cleaned)
expensive = (price for price in numeric if price > 10.0)

print("\n--- Prices above $10 ---")
for price in expensive:
    print(f"  ${price:.2f}")


# Practical application: student grade processing
student_records = [
    ("Alice", 92), ("Bob", 67), ("Charlie", 85),
    ("Diana", 45), ("Eve", 91), ("Frank", 73),
]

passing_students = (
    f"  {name}: {grade}"
    for name, grade in student_records
    if grade >= 70
)

print("\n--- Passing students (grade >= 70) ---")
for entry in passing_students:
    print(entry)

# Using any() and all() with generator expressions
all_passed = all(grade >= 50 for _, grade in student_records)
any_failed = any(grade < 50 for _, grade in student_records)

print(f"\n  Everyone scored >= 50? {all_passed}")
print(f"  Anyone scored < 50?   {any_failed}")
