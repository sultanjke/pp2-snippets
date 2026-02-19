# =============================================================
# Method Overriding with super() Usage
# =============================================================


# Base class with methods that children will override
class Employee:
    def __init__(self, full_name, base_salary):
        self.full_name = full_name
        self.base_salary = base_salary

    def calculate_pay(self):
        return self.base_salary

    def get_role(self):
        return "Employee"

    def summary(self):
        pay = self.calculate_pay()
        return f"{self.get_role()}: {self.full_name} -> ${pay:,.2f}/month"


# Overrides calculate_pay to add a bonus percentage
class Manager(Employee):
    def __init__(self, full_name, base_salary, bonus_percent):
        super().__init__(full_name, base_salary)
        self.bonus_percent = bonus_percent

    def calculate_pay(self):
        base_pay = super().calculate_pay()
        return base_pay + (base_pay * self.bonus_percent / 100)

    def get_role(self):
        return "Manager"


# Overrides calculate_pay to add commission on top of base
class SalesPerson(Employee):
    def __init__(self, full_name, base_salary, total_sales, commission_rate):
        super().__init__(full_name, base_salary)
        self.total_sales = total_sales
        self.commission_rate = commission_rate

    def calculate_pay(self):
        base_pay = super().calculate_pay()
        commission = self.total_sales * self.commission_rate / 100
        return base_pay + commission

    def get_role(self):
        return "Sales"


# Inherits from Manager and adds a department override
class Director(Manager):
    def __init__(self, full_name, base_salary, bonus_percent, department):
        super().__init__(full_name, base_salary, bonus_percent)
        self.department = department

    def get_role(self):
        return f"Director of {self.department}"


# summary() is defined ONCE in Employee but calls the overridden
# versions of calculate_pay() and get_role() — this is polymorphism
staff = [
    Employee("Bob", 3000),
    Manager("Alice", 5000, bonus_percent=20),
    SalesPerson("Charlie", 2500, total_sales=50000, commission_rate=5),
    Director("Diana", 7000, bonus_percent=25, department="Engineering"),
]

print("--- Payroll (method overriding in action) ---")
for person in staff:
    print(f"  {person.summary()}")


# ---- Practical Application: Notification System ----
# Each channel overrides send() but uses super().__init__ for shared setup

class Notification:
    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message
        self.sent = False

    def send(self):
        self.sent = True
        return f"[BASE] Sent to {self.recipient}"

    def status(self):
        state = "Sent" if self.sent else "Pending"
        return f"  {self.__class__.__name__} to {self.recipient}: {state}"


class EmailNotification(Notification):
    def __init__(self, recipient, message, subject):
        super().__init__(recipient, message)
        self.subject = subject

    def send(self):
        super().send()
        return f"[EMAIL] '{self.subject}' sent to {self.recipient}"


class SMSNotification(Notification):
    def __init__(self, recipient, message):
        super().__init__(recipient, message)
        # Truncate SMS to 160 characters
        if len(self.message) > 160:
            self.message = self.message[:157] + "..."

    def send(self):
        super().send()
        return f"[SMS] Sent to {self.recipient} ({len(self.message)} chars)"


class PushNotification(Notification):
    def __init__(self, recipient, message, device_token):
        super().__init__(recipient, message)
        self.device_token = device_token

    def send(self):
        super().send()
        return f"[PUSH] Sent to device {self.device_token[:8]}..."


notifications = [
    EmailNotification("sultan@example.com", "Your order shipped!", subject="Order Update"),
    SMSNotification("+7-701-123-4567", "Your code is 482910"),
    PushNotification("alice", "New message received", device_token="abc123def456"),
]

print("\n--- Sending notifications ---")
for notification in notifications:
    print(f"  {notification.send()}")

print("\n--- Status check ---")
for notification in notifications:
    print(notification.status())
