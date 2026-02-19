# =============================================================
# Class Definition, Object Creation, and the __init__ Constructor
# =============================================================
# A class is a blueprint for creating objects. Objects are
# instances of a class, each holding their own data.
#
# The __init__() method is a special "constructor" that runs
# automatically every time a new object is created. It sets up
# the object's initial state (its attributes).
# =============================================================


# --- Simplest possible class ---
# A class with no attributes or methods (just a container)
class Empty:
    pass


obj = Empty()
print("Empty object:", obj)
print("Type:", type(obj))


# --- Class with __init__: setting up initial state ---
# __init__ runs automatically when you create an object.
# 'self' refers to the specific object being created.
class Student:
    def __init__(self, name, age, major):
        # These are instance attributes — unique to each object
        self.name = name
        self.age = age
        self.major = major


# Creating objects (instances) of the Student class
student1 = Student("Sultan", 20, "Computer Science")
student2 = Student("Alice", 22, "Mathematics")

# Each object has its OWN copy of the attributes
print(f"\nStudent 1: {student1.name}, {student1.age}, {student1.major}")
print(f"Student 2: {student2.name}, {student2.age}, {student2.major}")


# --- __init__ with default parameter values ---
class Course:
    def __init__(self, title, code, credits=3):
        self.title = title
        self.code = code
        self.credits = credits  # Defaults to 3 if not provided


course1 = Course("Programming Principles", "CS201")
course2 = Course("Calculus II", "MATH202", 4)

print(f"\n{course1.code}: {course1.title} ({course1.credits} credits)")
print(f"{course2.code}: {course2.title} ({course2.credits} credits)")


# --- __init__ with validation logic ---
# The constructor can validate data before storing it
class BankAccount:
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        # Ensure balance can never start negative
        if initial_balance < 0:
            print(f"  Warning: negative balance not allowed, setting to 0.")
            self.balance = 0
        else:
            self.balance = initial_balance


acc1 = BankAccount("Sultan", 500)
acc2 = BankAccount("Alice", -100)  # Triggers the validation

print(f"\n{acc1.owner}'s balance: ${acc1.balance}")
print(f"{acc2.owner}'s balance: ${acc2.balance}")


# --- Creating multiple objects from the same class ---
# Each object is independent — changing one doesn't affect others
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


points = [Point(0, 0), Point(3, 4), Point(-1, 7)]

print("\n--- Points ---")
for i, p in enumerate(points):
    print(f"  Point {i}: ({p.x}, {p.y})")

# Changing one point doesn't affect the others
points[0].x = 99
print(f"\nAfter modifying Point 0: ({points[0].x}, {points[0].y})")
print(f"Point 1 is unchanged:    ({points[1].x}, {points[1].y})")


# =============================================================
# Practical Application: Building a Student Registry
# =============================================================
class RegistryStudent:
    def __init__(self, student_id, name, gpa=0.0):
        self.student_id = student_id
        self.name = name
        self.gpa = gpa


# Build a registry from raw data
raw_data = [
    (1001, "Sultan", 3.7),
    (1002, "Alice", 3.9),
    (1003, "Bob", 3.2),
    (1004, "Diana", 3.5),
]

registry = [RegistryStudent(sid, name, gpa) for sid, name, gpa in raw_data]

print("\n--- Student Registry ---")
print(f"  {'ID':<6} {'Name':<10} {'GPA'}")
print(f"  {'-' * 24}")
for s in registry:
    print(f"  {s.student_id:<6} {s.name:<10} {s.gpa}")
