# =============================================================
# Example 2: Function Arguments
#   - Positional arguments
#   - Default (optional) arguments
#   - *args  (variable-length positional arguments)
#   - **kwargs (variable-length keyword arguments)
# =============================================================


# Positional arguments
# Arguments are matched to parameters by their position.
def calculate_area(length, width):
    """Calculate the area of a rectangle."""
    return length * width


# 'length' gets 5, 'width' gets 3 based on position
print("Area of 5x3 rectangle:", calculate_area(5, 3))


# Default arguments
# You can assign default values so the caller can omit them.
def create_profile(name, age, city="Unknown"):
    """
    Build a user profile dictionary.

    'city' is optional and defaults to 'Unknown' if not provided.
    """
    return {"name": name, "age": age, "city": city}


# Calling with and without the default argument
print("\nWith city:   ", create_profile("Sultan", 20, "Almaty"))
print("Without city:", create_profile("Alice", 25))


# *args: accept any number of positional arguments
# *args collects extra positional arguments into a tuple.
def calculate_average(*args):
    """
    Return the average of all provided numbers.

    Args:
        *args: One or more numeric values.
    """
    if not args:
        return 0
    return sum(args) / len(args)


print("\n--- Using *args ---")
print("Average of 10, 20, 30:      ", calculate_average(10, 20, 30))
print("Average of 4, 8, 15, 16, 23:", calculate_average(4, 8, 15, 16, 23))
print("Average of a single value 7:", calculate_average(7))


# **kwargs: accept any number of keyword arguments
# **kwargs collects extra keyword arguments into a dictionary.
def print_order(**kwargs):
    """
    Display an order summary from keyword arguments.

    Args:
        **kwargs: Arbitrary order details as key=value pairs.
    """
    print("\n--- Order Summary ---")
    for key, value in kwargs.items():
        # Replace underscores with spaces for nicer output
        print(f"  {key.replace('_', ' ').title()}: {value}")


print_order(item="Laptop", price=999.99, quantity=1, shipping="Express")
print_order(item="Book", price=15.50, quantity=3)


# Combining all argument types in one function
# Order matters: positional -> default -> *args -> **kwargs
def build_report(title, author="Anonymous", *sections, **metadata):
    """
    Build a structured report combining all argument types.

    Args:
        title (str):     Report title (positional, required).
        author (str):    Author name (default: 'Anonymous').
        *sections:       Variable number of section names.
        **metadata:      Additional metadata as keyword arguments.
    """
    print(f"\n{'=' * 40}")
    print(f"  Report : {title}")
    print(f"  Author : {author}")

    if sections:
        print("  Sections:")
        for i, section in enumerate(sections, start=1):
            print(f"    {i}. {section}")

    if metadata:
        print("  Metadata:")
        for key, value in metadata.items():
            print(f"    {key}: {value}")
    print(f"{'=' * 40}")


build_report(
    "Python Functions Guide",
    "Sultan",
    "Basics", "Arguments", "Return Values",
    version="1.0", language="Python"
)
