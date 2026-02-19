# =============================================================
# Example 4: Passing Lists and Other Data Types as Arguments
# =============================================================
# Functions can accept any data type: lists, dictionaries, sets,
# tuples, etc.  Important: mutable objects (like lists and dicts)
# are passed by reference, meaning the function can modify the
# original object.  Immutable objects (int, str, tuple) cannot
# be changed inside the function.
# =============================================================


# --- Passing a list ---
def double_values(numbers):
    """
    Return a new list where every element is doubled.

    The original list is NOT modified (we build a new one).
    """
    return [n * 2 for n in numbers]


original = [1, 2, 3, 4, 5]
doubled = double_values(original)
print("Original list:", original)
print("Doubled list: ", doubled)


# --- Mutating a list inside a function ---
# Because lists are mutable, changes inside the function affect
# the original list.
def remove_negatives(numbers):
    """Remove all negative numbers from the list IN PLACE."""
    i = 0
    while i < len(numbers):
        if numbers[i] < 0:
            numbers.pop(i)  # Modifies the original list
        else:
            i += 1


data = [10, -3, 7, -1, 4, -8, 6]
print(f"\nBefore remove_negatives: {data}")
remove_negatives(data)
print(f"After  remove_negatives: {data}")  # Negatives are gone


# --- Passing a dictionary ---
def summarize_student(student):
    """
    Print a formatted summary of a student dictionary.

    Args:
        student (dict): Must contain 'name', 'age', and 'grades' keys.
    """
    name = student["name"]
    age = student["age"]
    grades = student["grades"]
    avg = sum(grades) / len(grades)
    print(f"\n--- Student Summary ---")
    print(f"  Name:          {name}")
    print(f"  Age:           {age}")
    print(f"  Grades:        {grades}")
    print(f"  Average grade: {avg:.1f}")


student_info = {
    "name": "Sultan",
    "age": 20,
    "grades": [90, 85, 92, 88],
}
summarize_student(student_info)


# --- Passing a set to remove duplicates ---
def common_elements(set_a, set_b):
    """
    Find and return elements that appear in both sets.

    Args:
        set_a (set): First set of items.
        set_b (set): Second set of items.

    Returns:
        set: Intersection of the two sets.
    """
    return set_a & set_b  # The & operator computes the intersection


languages_alice = {"Python", "Java", "C++", "Rust"}
languages_bob = {"Python", "Go", "Rust", "JavaScript"}

shared = common_elements(languages_alice, languages_bob)
print(f"\nAlice knows: {languages_alice}")
print(f"Bob knows:   {languages_bob}")
print(f"Both know:   {shared}")


# --- Practical example: a shopping cart processor ---
def process_cart(cart_items):
    """
    Calculate totals for a shopping cart.

    Args:
        cart_items (list[dict]): Each dict must have 'item', 'price',
                                 and 'quantity' keys.

    Returns:
        dict: Contains 'items_count', 'total_cost', and 'breakdown'.
    """
    breakdown = []
    total_cost = 0

    for entry in cart_items:
        subtotal = entry["price"] * entry["quantity"]
        total_cost += subtotal
        breakdown.append(f"  {entry['item']} x{entry['quantity']} = ${subtotal:.2f}")

    return {
        "items_count": sum(e["quantity"] for e in cart_items),
        "total_cost": total_cost,
        "breakdown": breakdown,
    }


cart = [
    {"item": "Notebook", "price": 5.50, "quantity": 3},
    {"item": "Pen",      "price": 1.20, "quantity": 10},
    {"item": "Backpack", "price": 35.00, "quantity": 1},
]

result = process_cart(cart)
print(f"\n--- Shopping Cart ---")
for line in result["breakdown"]:
    print(line)
print(f"  {'—' * 25}")
print(f"  Total items: {result['items_count']}")
print(f"  Total cost:  ${result['total_cost']:.2f}")
