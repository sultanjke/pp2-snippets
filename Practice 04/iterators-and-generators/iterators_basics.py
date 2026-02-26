# =============================================================
# Iterators Basics: iter(), next(), and Looping
# =============================================================

# Any iterable (list, tuple, string, dict, set) can produce
# an iterator using iter(), then be consumed with next().

fruits = ["apple", "banana", "cherry"]

fruit_iterator = iter(fruits)

print("--- Manual iteration with next() ---")
print(next(fruit_iterator))
print(next(fruit_iterator))
print(next(fruit_iterator))

# Calling next() again would raise StopIteration
try:
    next(fruit_iterator)
except StopIteration:
    print("StopIteration: no more items\n")


# Strings are iterable too
word = "Python"
letter_iterator = iter(word)

print("--- Iterating over a string ---")
print(next(letter_iterator))
print(next(letter_iterator))
print(next(letter_iterator))


# A for loop is just syntactic sugar for iter() + next()
# These two blocks do exactly the same thing:

print("\n--- for loop (under the hood) ---")
numbers = [10, 20, 30]

# What Python actually does internally:
numbers_iterator = iter(numbers)
while True:
    try:
        value = next(numbers_iterator)
        print(f"  got: {value}")
    except StopIteration:
        break

# What we normally write:
print("\n--- for loop (normal syntax) ---")
for value in numbers:
    print(f"  got: {value}")


# Iterating over a dictionary yields its keys by default
student_grades = {"Alice": 92, "Bob": 85, "Charlie": 78}

print("\n--- Iterating over dict keys ---")
for name in student_grades:
    print(f"  {name}: {student_grades[name]}")

# Use .items() to iterate over key-value pairs
print("\n--- Iterating over dict items ---")
for name, grade in student_grades.items():
    print(f"  {name}: {grade}")


# Practical application: reading data in chunks
print("\n--- Processing a log file line by line ---")
log_lines = [
    "INFO: Server started",
    "WARNING: High memory usage",
    "ERROR: Connection timeout",
    "INFO: Request processed",
    "ERROR: Disk full",
]

log_iterator = iter(log_lines)
error_count = 0

for line in log_iterator:
    if line.startswith("ERROR"):
        error_count += 1
        print(f"  Found error: {line}")

print(f"  Total errors: {error_count}")
