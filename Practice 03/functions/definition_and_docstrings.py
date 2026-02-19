# =============================================================
# Example 1: Function Definition, Calling, and Docstrings
# =============================================================
# A function is a reusable block of code that performs a
# specific task. You define it once and call it whenever needed.
# Docstrings document what a function does, its parameters,
# and what it returns.
# =============================================================


# Basic function definition and calling
# Use the 'def' keyword followed by a name and parentheses.
def greet():
    """Print a simple greeting message."""
    print("Hello! Welcome to the Functions tutorial.")


# Calling the function executes the code inside it
greet()


# Function with parameters and a docstring
def introduce(name, role):
    """
    Introduce a person with their role.

    Args:
        name (str): The person's name.
        role (str): The person's role or title.
    """
    print(f"My name is {name} and I am a {role}.")


introduce("Sultan", "student")
introduce("Alice", "developer")


# Docstrings are accessible at runtime via __doc__
print("\n--- Accessing docstrings programmatically ---")
print(f"greet.__doc__        -> {greet.__doc__}")
print(f"introduce.__doc__    -> {introduce.__doc__}")


# Practical example: a temperature converter
def celsius_to_fahrenheit(celsius):
    """
    Convert a temperature from Celsius to Fahrenheit.

    Args:
        celsius (float): Temperature in degrees Celsius.

    Returns:
        float: Temperature in degrees Fahrenheit.

    Example:
        >>> celsius_to_fahrenheit(0)
        32.0
        >>> celsius_to_fahrenheit(100)
        212.0
    """
    return celsius * 9 / 5 + 32


# Calling the converter and printing results
temps_c = [0, 20, 37, 100]
print("\n--- Celsius to Fahrenheit conversions ---")
for t in temps_c:
    print(f"  {t}°C  ->  {celsius_to_fahrenheit(t)}°F")
