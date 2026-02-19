# =============================================================
# Example 3: Return Values and Statements
# =============================================================
# Functions can return data back to the caller using 'return'.
# A function without a return statement returns None by default.
# You can return single values, multiple values (as a tuple),
# or use early returns to exit a function conditionally.
# =============================================================


# Single return value
def square(n):
    """Return the square of a number."""
    return n * n


result = square(6)
print("Square of 6:", result)


# A function without return gives None
def say_hello(name):
    """Print a greeting but return nothing."""
    print(f"Hello, {name}!")


returned = say_hello("Sultan")
print("Return value of say_hello:", returned)  # None


# Returning multiple values
# Python packs them into a tuple; you can unpack on the caller side.
def min_max_avg(numbers):
    """
    Compute the minimum, maximum, and average of a list.

    Args:
        numbers (list): A list of numeric values.

    Returns:
        tuple: (minimum, maximum, average)
    """
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    return minimum, maximum, average


scores = [85, 92, 78, 95, 88]
lo, hi, avg = min_max_avg(scores)  # Unpacking the returned tuple
print(f"\nScores: {scores}")
print(f"  Min: {lo}, Max: {hi}, Average: {avg}")


# Early return for input validation
# 'return' can exit the function immediately when a condition is met.
def divide(a, b):
    """
    Safely divide a by b.

    Returns None and prints a warning if b is zero.
    """
    if b == 0:
        print("  Warning: division by zero is not allowed.")
        return None  # Exit early — code below won't execute
    return a / b


print("\n--- Safe division ---")
print("  10 / 3  =", divide(10, 3))
print("  10 / 0  =", divide(10, 0))


# Practical example: a grade classifier
def classify_grade(score):
    """
    Convert a numeric score (0-100) into a letter grade.

    Returns:
        str: The letter grade, or an error message for invalid input.
    """
    if not 0 <= score <= 100:
        return "Invalid score"

    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


print("\n--- Grade classifier ---")
test_scores = [95, 82, 73, 61, 45, 110]
for s in test_scores:
    print(f"  Score {s:>3} -> Grade: {classify_grade(s)}")


# Returning a dictionary for structured data
def analyze_text(text):
    """
    Analyze a piece of text and return statistics as a dictionary.

    Returns:
        dict: Contains word_count, char_count, and unique_words.
    """
    words = text.lower().split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "unique_words": len(set(words)),
    }


sample = "Python is great and Python is fun"
stats = analyze_text(sample)
print(f"\n--- Text analysis for: \"{sample}\" ---")
for key, value in stats.items():
    print(f"  {key}: {value}")
