# =============================================================
# Instance Methods and the self Parameter
# =============================================================
# Instance methods are functions defined inside a class that
# operate on a specific object. The first parameter is always
# 'self', which refers to the object calling the method.
#
# Through 'self', a method can:
#   - Read the object's attributes   (self.name)
#   - Modify the object's attributes (self.balance = ...)
#   - Call other methods on the same object (self.other_method())
# =============================================================


# --- Basic instance methods ---
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.tricks = []  # Each dog starts with no tricks

    # 'self' lets the method access THIS specific dog's data
    def bark(self):
        print(f"{self.name} says: Woof!")

    def learn_trick(self, trick):
        self.tricks.append(trick)
        print(f"{self.name} learned '{trick}'!")

    def show_tricks(self):
        if self.tricks:
            print(f"{self.name} knows: {', '.join(self.tricks)}")
        else:
            print(f"{self.name} hasn't learned any tricks yet.")


dog1 = Dog("Rex", "German Shepherd")
dog2 = Dog("Bella", "Golden Retriever")

dog1.bark()
dog2.bark()

# Methods modify only the object they're called on
dog1.learn_trick("sit")
dog1.learn_trick("shake")
dog2.learn_trick("roll over")

print()
dog1.show_tricks()  # sit, shake
dog2.show_tricks()  # roll over (independent from dog1)


# --- Methods that return values ---
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height

    def describe(self):
        shape = "square" if self.is_square() else "rectangle"
        return f"{shape} {self.width}x{self.height} (area={self.area()}, perimeter={self.perimeter()})"


print("\n--- Rectangle methods ---")
r1 = Rectangle(5, 3)
r2 = Rectangle(4, 4)

print(f"  {r1.describe()}")
print(f"  {r2.describe()}")


# --- Methods that call other methods via self ---
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.history = []  # Track all transactions

    def deposit(self, amount):
        if amount <= 0:
            print("  Deposit amount must be positive.")
            return
        self.balance += amount
        self._record(f"Deposited ${amount:.2f}")  # Calls another method

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"  Insufficient funds for ${amount:.2f} withdrawal.")
            return
        self.balance -= amount
        self._record(f"Withdrew ${amount:.2f}")

    # A "helper" method — prefixed with _ to signal internal use
    def _record(self, description):
        self.history.append(description)

    def get_statement(self):
        print(f"\n--- Statement for {self.owner} ---")
        for entry in self.history:
            print(f"  {entry}")
        print(f"  Current balance: ${self.balance:.2f}")


account = BankAccount("Sultan", 1000)
account.deposit(250)
account.withdraw(100)
account.withdraw(75)
account.deposit(500)
account.get_statement()


# =============================================================
# Practical Application: Task Tracker
# =============================================================
class TaskTracker:
    def __init__(self, project_name):
        self.project_name = project_name
        self.tasks = []

    def add_task(self, title):
        self.tasks.append({"title": title, "done": False})
        print(f"  Added: '{title}'")

    def complete_task(self, title):
        for task in self.tasks:
            if task["title"] == title and not task["done"]:
                task["done"] = True
                print(f"  Completed: '{title}'")
                return
        print(f"  Task '{title}' not found or already done.")

    def pending_count(self):
        return sum(1 for t in self.tasks if not t["done"])

    def show_status(self):
        print(f"\n--- {self.project_name} ---")
        for task in self.tasks:
            status = "done" if task["done"] else "pending"
            mark = "x" if task["done"] else " "
            print(f"  [{mark}] {task['title']} ({status})")
        print(f"  Pending: {self.pending_count()} / {len(self.tasks)}")


tracker = TaskTracker("Python Course")
tracker.add_task("Learn variables")
tracker.add_task("Practice loops")
tracker.add_task("Study functions")
tracker.add_task("Master classes")

tracker.complete_task("Learn variables")
tracker.complete_task("Practice loops")

tracker.show_status()
