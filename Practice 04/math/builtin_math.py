# =============================================================
# Built-in Math Functions: min, max, abs, round, pow
# =============================================================

# min() and max() work on any iterable
scores = [78, 92, 65, 88, 95, 71]

print("--- min() and max() ---")
print(f"  Scores:  {scores}")
print(f"  Highest: {max(scores)}")
print(f"  Lowest:  {min(scores)}")

# With strings, they compare alphabetically
names = ["Charlie", "Alice", "Bob", "Diana"]
print(f"  First alphabetically: {min(names)}")
print(f"  Last alphabetically:  {max(names)}")

# Using key parameter for custom comparison
students = [
    {"name": "Alice", "gpa": 3.8},
    {"name": "Bob", "gpa": 3.2},
    {"name": "Charlie", "gpa": 3.9},
]
top_student = max(students, key=lambda s: s["gpa"])
print(f"  Top student: {top_student['name']} (GPA: {top_student['gpa']})")


# abs() returns the absolute value
print(f"\n--- abs() ---")
print(f"  abs(-15)   = {abs(-15)}")
print(f"  abs(7)     = {abs(7)}")
print(f"  abs(-3.14) = {abs(-3.14)}")

# Practical use: distance between two points on a number line
point_a, point_b = 12, -5
distance = abs(point_a - point_b)
print(f"  Distance between {point_a} and {point_b}: {distance}")


# round() rounds to a given number of decimal places
print(f"\n--- round() ---")
print(f"  round(3.14159)     = {round(3.14159)}")
print(f"  round(3.14159, 2)  = {round(3.14159, 2)}")
print(f"  round(3.14159, 4)  = {round(3.14159, 4)}")
print(f"  round(2.5)         = {round(2.5)}")    # Banker's rounding
print(f"  round(3.5)         = {round(3.5)}")    # Rounds to nearest even
print(f"  round(1234, -2)    = {round(1234, -2)}")  # Round to hundreds


# pow() raises a number to a power
print(f"\n--- pow() ---")
print(f"  pow(2, 8)      = {pow(2, 8)}")      # 2^8 = 256
print(f"  pow(5, 3)      = {pow(5, 3)}")      # 5^3 = 125
print(f"  pow(2, 10)     = {pow(2, 10)}")     # 2^10 = 1024
print(f"  pow(7, 2, 5)   = {pow(7, 2, 5)}")   # (7^2) % 5 = 49 % 5 = 4
print(f"  2 ** 8         = {2 ** 8}")          # ** operator does the same


# Practical application: grading summary
print(f"\n--- Grade summary ---")
grades = [72, 85, 91, 68, 95, 88, 79, 63, 97, 84]

average = sum(grades) / len(grades)
spread = max(grades) - min(grades)

print(f"  Grades:  {grades}")
print(f"  Count:   {len(grades)}")
print(f"  Sum:     {sum(grades)}")
print(f"  Average: {round(average, 1)}")
print(f"  Highest: {max(grades)}")
print(f"  Lowest:  {min(grades)}")
print(f"  Spread:  {spread}")
