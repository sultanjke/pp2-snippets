# =============================================================
# Class Variables vs Instance Variables
# =============================================================
# Instance variables  — defined in __init__ with self.xxx
#   - Each object gets its OWN independent copy
#   - Changing one object's value doesn't affect others
#
# Class variables — defined directly in the class body
#   - SHARED across ALL objects of that class
#   - Useful for counters, defaults, and shared configuration
# =============================================================


# --- Demonstrating the difference ---
class Student:
    # CLASS variable — shared by every Student object
    school = "KBTU"
    student_count = 0

    def __init__(self, name, gpa):
        # INSTANCE variables — unique to each object
        self.name = name
        self.gpa = gpa
        # Increment the shared counter each time an object is created
        Student.student_count += 1


s1 = Student("Sultan", 3.7)
s2 = Student("Alice", 3.9)
s3 = Student("Bob", 3.2)

# All students share the same school
print(f"{s1.name} goes to {s1.school}")
print(f"{s2.name} goes to {s2.school}")
print(f"{s3.name} goes to {s3.school}")

# The class variable tracks total objects created
print(f"\nTotal students created: {Student.student_count}")


# --- Key behavior: what happens when you assign through an object ---
print("\n--- Shadowing a class variable ---")
print(f"Before: s1.school = {s1.school}, s2.school = {s2.school}")

# This creates a NEW instance variable on s1, it does NOT
# change the class variable for everyone else
s1.school = "MIT"

print(f"After:  s1.school = {s1.school}, s2.school = {s2.school}")
print(f"Class:  Student.school = {Student.school}")
# s1 now has its own 'school'; s2 still reads the class variable


# --- Mutable class variables: a common pitfall ---
class TeamBad:
    # WARNING: mutable class variable is shared by reference!
    members = []

    def __init__(self, name):
        self.name = name
        self.members.append(name)  # Modifies the SHARED list


class TeamGood:
    # CORRECT: use __init__ to give each object its own list
    team_count = 0

    def __init__(self, name, members=None):
        self.name = name
        self.members = members if members is not None else []
        TeamGood.team_count += 1


print("\n--- Mutable class variable pitfall ---")
t1 = TeamBad("Alpha")
t2 = TeamBad("Beta")
# Both teams share the SAME list — unintended!
print(f"  TeamBad t1.members: {t1.members}")
print(f"  TeamBad t2.members: {t2.members}")  # Also has 'Alpha'!

print("\n--- Correct approach with instance variables ---")
g1 = TeamGood("Alpha", ["Alice", "Bob"])
g2 = TeamGood("Beta", ["Charlie"])
print(f"  TeamGood g1.members: {g1.members}")
print(f"  TeamGood g2.members: {g2.members}")  # Independent


# --- Using class variables for shared configuration ---
class APIClient:
    # Shared configuration — same for all instances
    base_url = "https://api.example.com"
    timeout = 30
    max_retries = 3

    def __init__(self, endpoint):
        # Instance variable — unique per client
        self.endpoint = endpoint

    def full_url(self):
        return f"{self.base_url}/{self.endpoint}"

    def describe(self):
        return (
            f"  {self.full_url()} "
            f"(timeout={self.timeout}s, retries={self.max_retries})"
        )


print("\n--- Shared config via class variables ---")
users_api = APIClient("users")
orders_api = APIClient("orders")

print(users_api.describe())
print(orders_api.describe())

# Change config once — affects all instances
APIClient.timeout = 60
print("\nAfter updating APIClient.timeout to 60:")
print(users_api.describe())
print(orders_api.describe())


# =============================================================
# Practical Application: Product Inventory with Tracking
# =============================================================
class Product:
    # Class variables for shared tracking
    total_products = 0
    category_counts = {}

    def __init__(self, name, category, price):
        # Instance variables for individual product data
        self.name = name
        self.category = category
        self.price = price

        # Update shared trackers
        Product.total_products += 1
        Product.category_counts[category] = (
            Product.category_counts.get(category, 0) + 1
        )

    @classmethod
    def inventory_summary(cls):
        print(f"\n--- Inventory Summary ---")
        print(f"  Total products: {cls.total_products}")
        print(f"  By category:")
        for cat, count in cls.category_counts.items():
            print(f"    {cat}: {count}")


# Create products — class variables track everything automatically
Product("Laptop", "Electronics", 999)
Product("Mouse", "Electronics", 25)
Product("Desk", "Furniture", 200)
Product("Chair", "Furniture", 150)
Product("Headset", "Electronics", 60)
Product("Lamp", "Furniture", 35)
Product("Python Book", "Books", 30)

Product.inventory_summary()
