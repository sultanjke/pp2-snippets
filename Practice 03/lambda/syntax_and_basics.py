# =============================================================
# Lambda Syntax and Basic Usage
# =============================================================
# A lambda is a small, anonymous (unnamed) function written in
# a single line using the 'lambda' keyword.
#
# Syntax:  lambda arguments: expression
#
# - Can take any number of arguments
# - Body is limited to ONE expression (no statements)
# - The expression's result is automatically returned
# =============================================================


# --- Simplest lambda: one argument ---
double = lambda x: x * 2

print("double(5):", double(5))
print("double(13):", double(13))


# --- Lambda with multiple arguments ---
add = lambda a, b: a + b
multiply = lambda a, b: a * b

print("\n--- Multiple arguments ---")
print("add(3, 7)     =", add(3, 7))
print("multiply(4, 5) =", multiply(4, 5))


# --- Lambda with no arguments ---
greet = lambda: "Hello, World!"
print("\nNo-arg lambda:", greet())


# --- Lambda with default argument values ---
power = lambda base, exp=2: base ** exp

print("\n--- Default arguments ---")
print("power(5)    =", power(5))      # Uses default exp=2 -> 25
print("power(5, 3) =", power(5, 3))   # Overrides exp to 3 -> 125


# --- Conditional (ternary) expression inside a lambda ---
# Lambdas can use inline if/else for simple branching
is_even = lambda n: "Even" if n % 2 == 0 else "Odd"

print("\n--- Conditional lambda ---")
for num in range(1, 7):
    print(f"  {num} -> {is_even(num)}")


# --- Calling a lambda immediately without assigning it ---
# Useful for quick one-time computations
result = (lambda x, y: x ** y)(2, 10)
print(f"\nImmediate call: 2^10 = {result}")


# --- String operations with lambda ---
shout = lambda text: text.upper() + "!"
whisper = lambda text: text.lower() + "..."

print("\n--- String lambdas ---")
print(shout("hello"))       # HELLO!
print(whisper("GOODBYE"))   # goodbye...


# =============================================================
# Practical Application: Quick Unit Converter
# =============================================================
# Store conversion formulas as lambdas in a dictionary for
# fast, readable access.

converters = {
    "km_to_miles": lambda km: round(km * 0.621371, 2),
    "kg_to_pounds": lambda kg: round(kg * 2.20462, 2),
    "celsius_to_f": lambda c: round(c * 9 / 5 + 32, 1),
}

print("\n--- Unit Converter ---")
print(f"  10 km     = {converters['km_to_miles'](10)} miles")
print(f"  75 kg     = {converters['kg_to_pounds'](75)} pounds")
print(f"  37°C      = {converters['celsius_to_f'](37)}°F")
